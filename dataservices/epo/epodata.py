from utilities.pdftools.pdftools import PdfMerger

__author__ = 'Eyal Fisher'

import re
import urllib
import os
import time
import threading
import xml.etree.ElementTree as ET

from multiprocessing.pool import ThreadPool
from epoclient import RegisteredClient
from utilities.sorting_utilities.sorting_utilities import NaturalSortingStrategy

class AuthenticationInfo():

    @staticmethod
    def get_key():
        return 'DDX2ve6YZZR5Zr8ADuEQ003qpA3xoHFS'

    @staticmethod
    def get_secret():
        return 'LK6lBYaK2BgfTtUp'


class Patent:

    def __init__(self, doc_number='', exchange_document=None, consumer_key='', consumer_secret='', reference_format=''):

        if consumer_key == '':
            consumer_key = AuthenticationInfo.get_key()
        if consumer_secret == '':
            consumer_secret = AuthenticationInfo.get_secret()

        if exchange_document is None:
            epo_client = RegisteredClient(consumer_key, consumer_secret)

            normalized_document_id = self.normalize_doc_id(doc_number)
            if reference_format == 'EPODOC':
                self.xml = epo_client.fetch_publication_xml_by_publication_reference(normalized_document_id).content
            else:
                self.xml = epo_client.fetch_publication_xml(normalized_document_id).content
            self.root = ET.fromstring(self.xml)
            self.exchange_document = self.root.iter(self.get_full_element_name('exchange-document')).next()

        else:
            self.exchange_document = exchange_document

    @staticmethod
    def normalize_doc_id(document_id):
        normalized_doc_id = re.sub("\W", "", document_id)
        return normalized_doc_id

    def get_title(self):
        try:
            return self.exchange_document.iter(self.get_full_element_name('invention-title')).next().text
        except StopIteration:
            return None

    def get_doc_number(self):
        return self.exchange_document.get('doc-number')

    def get_kind(self):
        return self.exchange_document.get('kind')

    def get_country(self):
        return self.exchange_document.get('country')

    def get_family_id(self):
        return self.exchange_document.get('family-id')

    def get_publication_reference(self):
        publication_reference_element = self.exchange_document.iter(
            self.get_full_element_name('publication-reference')).next()
        document_id_type_attribute = 'document-id-type'

        for child in publication_reference_element.iter(self.get_full_element_name('document-id')):
            if child.get(document_id_type_attribute) == 'docdb':
                docdb_publication_reference = self._get_docdb_publication_reference(child)

            if child.get(document_id_type_attribute) == 'epodoc':
                epodoc_publication_reference = self._get_epodoc_publication_reference(child)

        publication_reference = {
            'DOCDB': docdb_publication_reference,
            'EPODOC': epodoc_publication_reference
        }

        return publication_reference

    def _get_docdb_publication_reference(self, document_id_element):
        docdb_publication = {
            'country': self._get_child_text(document_id_element, 'country'),
            'doc-number': self._get_child_text(document_id_element, 'doc-number'),
            'kind': self._get_child_text(document_id_element, 'kind'),
            'date': self._get_child_text(document_id_element, 'date')
        }

        return docdb_publication

    def _get_epodoc_publication_reference(self, document_id_element):
        epodoc_publication = {
            'doc-number': self._get_child_text(document_id_element, 'doc-number'),
            'date': self._get_child_text(document_id_element, 'date')
        }

        return epodoc_publication

    def get_patent_classifications(self):
        classifications = {}
        self._get_irpc_classifications(classifications)
        self._get_cpc_and_uc_classifications(classifications)

        return classifications

    def _get_irpc_classifications(self, classifications):
        classifications['IRPC'] = []
        for child in self.exchange_document.iter(self.get_full_element_name('classification-ipcr')):
            classification_text = child.find(self.get_full_element_name('text')).text
            classifications['IRPC'].append(self._remove_multiple_spaces(classification_text))

        return classifications

    def _get_cpc_and_uc_classifications(self, classifications):
        classifications['CPC'] = []
        classifications['UC'] = []
        for child in self.exchange_document.iter(self.get_full_element_name('patent-classification')):
            classification_scheme = child.find(self.get_full_element_name('classification-scheme')).get('scheme')
            if classification_scheme == 'CPC':
                classifications['CPC'].append(self._get_cpc_classification(child))

            if classification_scheme == 'UC':
                classifications['UC'].append(self._get_uc_classification(child))

        return classifications

    def _get_cpc_classification(self, child):
        cpc_classification = {
            'section': self._get_classification_attribute(child, 'section'),
            'class': self._get_classification_attribute(child, 'class'),
            'subclass': self._get_classification_attribute(child, 'subclass'),
            'main-group': self._get_classification_attribute(child, 'main-group'),
            'subgroup': self._get_classification_attribute(child, 'subgroup'),
            'classification-value': self._get_classification_attribute(child, 'classification-value')
        }
        return cpc_classification

    def _get_classification_attribute(self, element, attribute):
        return element.find(self.get_full_element_name(attribute)).text

    def _get_uc_classification(self, child):
        return child.find(self.get_full_element_name('classification-symbol')).text

    def get_application_reference(self):
        application_reference_element = self._get_application_reference_element().next()

        docdb_application_reference = self._get_docdb_application_reference(application_reference_element)
        epodoc_application_reference = self._get_epodoc_document_id(application_reference_element)
        original_application = self.document_id(application_reference_element)

        application_reference = {
            # 'RID': self.get_application_RID(),
            'DOCDB': docdb_application_reference,
            'EPODOC': epodoc_application_reference,
            'ORIGINAL': original_application
        }

        return application_reference

    def get_application_RID(self):
        return self.exchange_document.iter(self.get_full_element_name('application-reference')).next().get('doc-id')

    def _get_document_id(self):
        doc_id = self.exchange_document.iter(self.get_full_element_name('document-id')).next()
        if doc_id.get('document-id-type') != 'docdb':
            raise NotImplementedError('only docdb is supported at this moment')

        return doc_id

    def _get_application_reference_element(self):
        return self.exchange_document.iter(self.get_full_element_name('application-reference'))

    def _get_docdb_application_reference(self, application_reference_element):
        docdb_document_id = self._get_document_id_element(application_reference_element, 'docdb')
        if docdb_document_id is None:
            return None

        docdb_application = {
            'country': self._get_child_text(docdb_document_id, 'country'),
            'doc-number': self._get_child_text(docdb_document_id, 'doc-number'),
            'kind': self._get_child_text(docdb_document_id, 'kind'),
        }

        return docdb_application

    def _get_document_id_element(self, application_reference_element, type):
        document_ids = application_reference_element.findall(self.get_full_element_name('document-id'))
        for document_id in document_ids:
            if document_id.get('document-id-type') == type:
                return document_id

        return None

    def _get_epodoc_document_id(self, application_reference_element):
        epodoc_document_id = self._get_document_id_element(application_reference_element, 'epodoc')
        if epodoc_document_id is None:
            return None

        epodoc_application = {
            'doc-number': self._get_child_text(epodoc_document_id, 'doc-number'),
            'date': self._get_child_text(epodoc_document_id, 'date')
        }

        return epodoc_application

    def document_id(self, application_reference_element):
        original_document_id = self._get_document_id_element(application_reference_element, 'original')
        if original_document_id is None:
            return None

        original_application = {
            'doc-number': self._get_child_text(original_document_id, 'doc-number')
        }

        return original_application

    def get_priority_claims(self):
        priority_claims = []
        for child in self.exchange_document.iter(self.get_full_element_name('priority-claim')):
            epodoc_claim = self._get_epodoc_document_id(child)
            original_claim = self.document_id(child)

            priority_claims.append(
                {
                    # 'kind': child.get('kind'),
                    'EPODOC': epodoc_claim,
                    'ORIGINAL': original_claim
                }
            )

        return priority_claims

    def _get_original_priority_claim(self, document_id):
        original_claim = {
            'doc-number': document_id.find(self.get_full_element_name('doc-number')).text
        }

        return original_claim

    def get_applicant_names(self):
        names = []
        for child in self.exchange_document.iter(self.get_full_element_name('applicant')):
            if child.get('data-format') == 'epodoc':
                names.append(child.iter(self.get_full_element_name('name')).next().text)

        return names

    def get_inventors_names(self):
        names = []
        for child in self.exchange_document.iter(self.get_full_element_name('inventor')):
            if child.get('data-format') == 'epodoc':
                names.append(child.iter(self.get_full_element_name('name')).next().text)

        return names

    def get_citations(self):
        citations = []
        for citation_element in self.exchange_document.iter(self.get_full_element_name('citation')):
            for document_id in citation_element.iter(self.get_full_element_name('document-id')):
                if document_id.get('document-id-type') == 'epodoc':
                    citations.append(document_id.find(self.get_full_element_name('doc-number')).text)

        return citations

    def get_abstract(self):
        abstract_element = self.exchange_document.iter(self.get_full_element_name('abstract')).next()
        abstract_string = ""

        for child in abstract_element.findall(self.get_full_element_name('p')):
            abstract_string = abstract_string + child.text

        return abstract_string

    def get_events(self):
        events_fetcher = EventFetcher()
        publication_reference = self.get_publication_reference()

        ## get_events uses epodoc publication reference at the moment.
        assert publication_reference.has_key('EPODOC')

        return events_fetcher.get_events_by_reference(publication_reference['EPODOC']['doc-number'])

    def _get_child_text(self, document_id_element, child_tag):
        return document_id_element.find(self.get_full_element_name(child_tag)).text

    @staticmethod
    def get_full_element_name(element):
        return '{http://www.epo.org/exchange}' + element

    @staticmethod
    def _remove_multiple_spaces(string):
        return ' '.join(string.split())


class EventFetcher:

    def __init__(self):
        self.epo_client = RegisteredClient(AuthenticationInfo.get_key(), AuthenticationInfo.get_secret())

    def get_events_by_reference(self, reference_number):
        events_xml = self.epo_client.fetch_events_xml_by_reference_number(reference_number).content
        events_root = ET.fromstring(events_xml)

        events = []
        for event_element in events_root.iter(self.get_full_element_name('dossier-event')):
            events.append({
                'event_date': event_element.iter(self.get_full_element_name('date')).next().text,
                'event_code': event_element.find(self.get_full_element_name('event-code')).text,
                'event_text': event_element.find(self.get_full_element_name('event-text')).text
            })

        return events

    @staticmethod
    def get_full_element_name(element_name):
        return '{http://www.epo.org/register}' + element_name


class Applicant:
    def __init__(self, applicant_name):
        self.fetching_url = 'http://ops.epo.org/3.1/rest-services/published-data/search/full-cycle/'
        self.applicant_name = applicant_name

    def get_patents(self):
        xml = self._get_result_set(1, 100)
        xml_root = ET.fromstring(xml)
        result_count = self._get_result_count(xml_root)
        first_result = 101
        last_result = 200
        results_interval = 100
        patents = []
        self._get_all_child_patents(patents, xml_root)
        i = 1
        while last_result - results_interval < result_count:
            xml = self._get_result_set(first_result, last_result)
            xml_root = ET.fromstring(xml)
            self._get_all_child_patents(patents, xml_root)

            first_result = last_result + 1
            last_result = last_result + results_interval
        return patents

    def _get_all_child_patents(self, patents, xml_root):
        for patent_exchange_document in xml_root.iter(Patent.get_full_element_name('exchange-document')):
            patent = Patent(exchange_document=patent_exchange_document)
            patents.append(patent)

    def _get_result_set(self, first_index, last_index):
        consumer_key = AuthenticationInfo.get_key()
        consumer_secret = AuthenticationInfo.get_secret()

        epo_client = RegisteredClient(consumer_key, consumer_secret)

        xml = epo_client.fetch_applicant_xml(self.applicant_name, first_index, last_index).content
        return xml

    def _get_result_count(self, xml_root):
        result_count_string = xml_root.iter(self.get_full_element_name('biblio-search')).next().get('total-result-count')
        return int(result_count_string)

    @staticmethod
    def get_full_element_name(element_name):
        return '{http://ops.epo.org}' + element_name


class EPOImages():

    def __init__(self, epo_doc_publication_number, consumer_key='', consumer_secret=''):

        if consumer_key == '':
            consumer_key = AuthenticationInfo.get_key()
        if consumer_secret == '':
            consumer_secret = AuthenticationInfo.get_secret()

        epo_client = RegisteredClient(consumer_key, consumer_secret)

        self.publication_number = epo_doc_publication_number

        self.xml = epo_client.fetch_image_information_xml(epo_doc_publication_number).content
        self.xml_root = ET.fromstring(self.xml)

    def get_number_of_pages_from_inquiry_result(self, inquiry_result):
        return int(inquiry_result.iter(self._get_full_element_name('document-instance')).next().get('number-of-pages'))

    def get_kind_from_inquiry_result(self, inquiry_result):
        return inquiry_result.iter(self._get_full_exchange_element_name('kind')).next().text

    def get_inquiry_results(self):
        return self.xml_root.iter(self._get_full_element_name('inquiry-result'))

    def get_number_of_pages(self):
        result = {}
        for inquiry_result in self.get_inquiry_results():
            kind = self.get_kind_from_inquiry_result(inquiry_result)
            number_of_pages = self.get_number_of_pages_from_inquiry_result(inquiry_result)

            result[kind] = number_of_pages

        return result

    def get_page(self, kind, page_number):
        url = 'http://ops.epo.org/rest-services/published-data/images/%s/%s/%s/fullimage.pdf?Range=%s' %\
              (self.get_country_code(),
               self.get_doc_number(),
               kind,
               page_number)

        urllib.urlretrieve(url, 'temp/%s-%s.pdf' % (kind, page_number))

    def get_page_x(self, kind_and_page_number):
        kind, page_number = kind_and_page_number

        self.get_page(kind, page_number)
        time.sleep(3)

    def get_all_pages_for_kind(self, kind):
        number_of_pages = self.get_number_of_pages()[kind]

        pool = ThreadPool(1)
        pool.map(self.get_page_x, [(kind, page_num) for page_num in range(1, number_of_pages + 1)])

    def get_all_pages(self):
        kinds = self.get_kinds()
        for kind in kinds:
            self.get_all_pages_for_kind(kind)


    def list_full_path(self, relative_directory):
        return [os.path.join(relative_directory, f) for f in os.listdir(relative_directory)]

    def get_publication_pdf(self, filepath):
        self.get_all_pages()
        pages = NaturalSortingStrategy().sort(self.list_full_path('temp'))

        pdf_merger = PdfMerger()

        pdf_merger.merge_pdf(pages, filepath)

    def get_kinds(self):
        return self.get_number_of_pages().keys()

    def get_country_code(self):
        return self.publication_number[0:2]

    def get_doc_number(self):
        return self.publication_number[2:]

    def _get_full_element_name(self, element_name):
        return '{http://ops.epo.org}' + element_name

    def _get_full_exchange_element_name(self, element_name):
        return '{http://www.epo.org/exchange}' + element_name




