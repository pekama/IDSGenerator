import requests

from bs4 import BeautifulSoup
from datetime import datetime
from dataservices.epo.epodata import Patent, EPOImages


class USPTOClient():

    def get_us_patent_html(self, patent_number):
        url = 'http://patft.uspto.gov/netacgi/nph-Parser?Sect2=PTO1&Se' \
              'ct2=HITOFF&p=1&u=/netahtml/PTO/search-bool.html&r=1&f=G&l=50&d=PALL&RefSrch=yes&Query=PN/%s' % (patent_number,)

        return self._get_html_from_url(url)

    def get_us_publication_html(self, application_number):
        url = 'http://appft1.uspto.gov/netacgi/nph-Parser?' \
              'Sect1=PTO1&Sect2=HITOFF&d=PG01&p=1&u=/netahtml/PTO/srchnum.html&r=1&f=G&l=50&s1=%s.PGNR.' % (application_number,)

        return self._get_html_from_url(url)

    def _get_html_from_url(self, url):
        response = requests.get(url)
        return response.content


class USPTOExtractDateMixin():

    def normalize_date(self, date_text):
        date_object = datetime.strptime(date_text, '%B %d, %Y')
        normalized_date = '{d.month}/{d.day}/{d.year}'.format(d=date_object)
        return normalized_date

    def get_date(self):
        date_element = self.metadata_row.find_all('td')[1].b
        date_text = date_element.text.strip()

        return self.normalize_date(date_text)


class USPTOPatent(USPTOExtractDateMixin):

    def __init__(self, patent_number, uspto_client=USPTOClient()):
        self.html = uspto_client.get_us_patent_html(patent_number)
        self.soup = BeautifulSoup(self.html)

        metadata_table = self.soup.find_all('table')[2]
        self.metadata_row = metadata_table.find_all('tr')[1]

    def get_inventor(self):
        inventor_text = self.metadata_row.td.b.text

        # remove unnecessary spaces:
        inventor_name = ' '.join([part.strip() for part in inventor_text.split(',')])

        return inventor_name


class USPTOPublication(USPTOExtractDateMixin):

    def __init__(self, application_number, uspto_client=USPTOClient()):
            self.html = uspto_client.get_us_publication_html(application_number)
            self.soup = BeautifulSoup(self.html)

            self.metadata_table = self.soup.find_all('table')[1]
            self.metadata_row = self.metadata_table.find_all('tr')[2]

    def normalize_applicant_name(self, applicant_text):
        # remove unnecessary spaces chars
        not_letters_or_digits = u'\n;'
        translate_table = dict((ord(char), u'') for char in not_letters_or_digits)
        applicant_name = applicant_text.translate(translate_table)

        # and unnecessary spaces
        applicant_name = ' '.join(applicant_name.split())
        return applicant_name

    def get_applicant(self):
        applicant_text = self.metadata_row.td.b.text

        applicant_name = self.normalize_applicant_name(applicant_text)

        return applicant_name


class ForeignPublication():

    def __init__(self, publication_number):
        self.EPO_COSTUMER_KEY = 'DDX2ve6YZZR5Zr8ADuEQ003qpA3xoHFS'
        self.EPO_COSTUMER_SECRET = 'LK6lBYaK2BgfTtUp'

        self.publication_number = publication_number
        self.epo_patent = Patent(publication_number, consumer_key=self.EPO_COSTUMER_KEY, consumer_secret=self.EPO_COSTUMER_SECRET)

    def get_applicant(self):
        applicants = self.epo_patent.get_applicant_names()
        first_applicant = applicants[0]

        return self._replace_unicode_space(first_applicant)

    def _replace_unicode_space(self, string):
        return string.replace(u'\u2002', u' ')

    def get_date(self):
        publication_reference = self.epo_patent.get_publication_reference()
        epo_date = publication_reference['DOCDB']['date']

        return self._normalize_date(epo_date)

    @staticmethod
    def _normalize_date(date_text):
        year = int(date_text[0:4])
        month = int(date_text[4:6])
        day = int(date_text[6:8])

        date_object = datetime(year, month, day)
        normalized_date = '{d.month}/{d.day}/{d.year}'.format(d=date_object)
        return normalized_date

    def get_publication_pdf(self, output_path):
        epo_images = EPOImages(self.publication_number, self.EPO_COSTUMER_KEY, self.EPO_COSTUMER_KEY)

        epo_images.get_publication_pdf(output_path)
