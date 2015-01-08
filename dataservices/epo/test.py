# -*- coding: utf-8 -*-

__author__ = 'Usuario'

from unittest import TestCase

from epodata import Patent, Applicant, EPOImages
import os

class TestEpoDataHelper(TestCase):

    def test_normalize_document_id(self):
        bad_doc_id = 'US 2013-0040049 A1'
        bad_doc_id2 = 'US /2013-0040048 A1'
        normalized_doc_id = Patent.normalize_doc_id(bad_doc_id)
        normalized_doc_id2 = Patent.normalize_doc_id(bad_doc_id2)

        self.assertEqual(normalized_doc_id, 'US20130040049A1')
        self.assertEqual(normalized_doc_id2, 'US20130040048A1')


class TestEPOFetching(TestCase):

    def setUp(self):
        self.patent = Patent('US2008182176')
        self.patent2 = Patent('EP2294260')

    def test_get_kind(self):
        self.assertEqual('A1', self.patent.get_kind())

    def test_get_country(self):
        self.assertEqual('US', self.patent.get_country())

    def test_get_abstract(self):
        abstract = self.patent.get_abstract()
        self.assertTrue(abstract.startswith('This invention'))
        self.assertTrue(abstract.endswith('lower than 2.'))

    def test_get_family_id(self):
        self.assertEqual('39668377', self.patent.get_family_id())

    def test_get_publication_reference(self):
        publication_reference = self.patent.get_publication_reference()

        self.assertEqual(publication_reference['DOCDB']['country'], 'US')
        self.assertEqual(publication_reference['DOCDB']['doc-number'], '2008182176')
        self.assertEqual(publication_reference['DOCDB']['kind'], 'A1')
        self.assertEqual(publication_reference['DOCDB']['date'], '20080731')

        self.assertEqual(publication_reference['EPODOC']['doc-number'], 'US2008182176')
        self.assertEqual(publication_reference['EPODOC']['date'], '20080731')


    def test_get_patent_classification(self):
        patent_classifications = self.patent.get_patent_classifications()

        self.assertEqual(patent_classifications['IRPC'][0], 'B22F 7/ 04 A I')

        self.assertEqual(len(patent_classifications['CPC']), 23)
        self.assertEqual(patent_classifications['CPC'][0]['section'], 'B')
        self.assertEqual(patent_classifications['CPC'][0]['class'], '82')
        self.assertEqual(patent_classifications['CPC'][0]['subclass'], 'Y')
        self.assertEqual(patent_classifications['CPC'][0]['main-group'], '30')
        self.assertEqual(patent_classifications['CPC'][0]['subgroup'], '00')
        self.assertEqual(patent_classifications['CPC'][0]['classification-value'], 'I')

        self.assertEqual(len(patent_classifications['UC']), 6)
        self.assertEqual(patent_classifications['UC'][0], '29/623.1')

    def test_get_application_reference(self):
        self.assertEqual(self.patent.get_application_reference()['RID'], '54051634')

        self.assertEqual(self.patent.get_application_reference()['DOCDB']['country'], 'US')
        self.assertEqual(self.patent.get_application_reference()['DOCDB']['doc-number'], '89931907')
        self.assertEqual(self.patent.get_application_reference()['DOCDB']['kind'], 'A')

        self.assertEqual(self.patent.get_application_reference()['EPODOC']['doc-number'], 'US20070899319')
        self.assertEqual(self.patent.get_application_reference()['EPODOC']['date'], '20070905')

        self.assertEqual(self.patent.get_application_reference()['ORIGINAL']['doc-number'], '11899319')

    def test_get_priority_claims(self):
        claims = self.patent.get_priority_claims()
        claim = claims[0]

        self.assertEqual(len(claims), 3)
        self.assertEqual(claim['kind'], 'national')

        self.assertEqual(claim['EPODOC']['doc-number'], 'US20070899319')
        self.assertEqual(claim['EPODOC']['date'], '20070905')

        self.assertEqual(claim['ORIGINAL']['doc-number'], '60897255')

    def test_get_applicants(self):
        applicant_names = self.patent2.get_applicant_names()
        self.assertEqual(len(applicant_names), 1)
        self.assertEqual(applicant_names[0], u'UNIV BAR ILAN [IL]')

    def test_get_inventors(self):
        self.assertEqual(8, len(self.patent.get_inventors_names()))
        self.assertEqual(5, len(self.patent2.get_inventors_names()))

    def test_get_title(self):
        self.assertEqual(self.patent.get_title(), 'Rechargeable magnesium battery')

    def test_get_citation(self):
        citations = self.patent.get_citations()

        self.assertEqual(len(citations), 4)
        self.assertEqual(citations[0], 'US3864167')

    def test_get_events(self):
        events = Patent('EP2294260').get_events()
        event = events[4]

        self.assertEqual(event['event_date'], '20120704')
        self.assertEqual(event['event_code'], 'EPIDOSNRFE2')
        self.assertEqual(event['event_text'], 'New entry: Renewal fee paid')


class TestApplicants(TestCase):

    def setUp(self):
        self.applicant = Applicant('IDE Technologies')
        self.patents = self.applicant.get_patents()

    def test_fetch_all_patents(self):
        self.assertEqual(self.patents[3].get_publication_reference()['EPODOC']['doc-number'], 'CA2854056')

# TODO: add tests to make sure all pages of results are fetched


class TestImages(TestCase):

    def setUp(self):
        self.images = EPOImages('WO2012012591')
        self._clear_temp()

    def tearDown(self):
        self._clear_temp()

    def _clear_temp(self):
        for pdf in os.listdir('temp'):
            os.remove('temp/' + pdf)

    def test_get_number_of_pages(self):
        self.assertEqual(self.images.get_number_of_pages()['A3'], 5)
        self.assertEqual(self.images.get_number_of_pages()['A2'], 63)

    def test_get_country_code(self):
        self.assertEqual(self.images.get_country_code(), 'WO')

    def test_get_doc_number(self):
        self.assertEqual(self.images.get_doc_number(), '2012012591')

    def test_get_page(self):
        self.images.get_page('A2', 1)
        self.assertTrue(os.path.isfile('temp/A2-1.pdf'))

    def test_get_all_pages_for_kind(self):
        self.images.get_all_pages_for_kind('A3')

        files = os.listdir('temp')

        self.assertEqual(len(files), 5)

    def test_get_all_pages(self):
        self.images.get_all_pages()

        files = os.listdir('temp')

        self.assertEqual(len(files), 68)

    def test_get_publication_pdf(self):
        self.images.get_publication_pdf(os.path.abspath('temp.pdf'))
        self.assertTrue(os.path.isfile('temp.pdf'))

        os.remove('temp.pdf')

