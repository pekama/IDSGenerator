from unittest import TestCase
from dataservices.uspto.USPTOdata import USPTOClient, USPTOPatent, USPTOPublication, USPTOExtractDateMixin, ForeignPublication


class MockUSPTOClient(USPTOClient):
    def __init__(self):
        self.patent_html = open('test_patent_page.html').read()
        self.publication_html = open('test_publication_page.html').read()

    def get_us_patent_html(self, patent_number):
        return self.patent_html

    def get_us_publication_html(self, application_number):
        return self.publication_html


class USPTOPatentTests(TestCase):

    def setUp(self):
        self.client = MockUSPTOClient()
        self.patent = USPTOPatent('7532932', uspto_client=self.client)

    def test_get_inventor(self):
        extracted_inventor = self.patent.get_inventor()
        self.assertEqual(extracted_inventor, 'Denker et al.')

    def test_get_date(self):
        extracted_date = self.patent.get_date()
        self.assertEqual(extracted_date, '5/12/2009')


class USPTOApplicationTests(TestCase):

    def setUp(self):
        self.client = MockUSPTOClient()
        self.publication = USPTOPublication('20070067007', uspto_client=self.client)

    def test_get_applicant(self):
        expected_applicant = 'Schulman Joseph H. et al.'
        actual_applicant = self.publication.get_applicant()

        self.assertEqual(actual_applicant, expected_applicant)

    def test_get_date(self):
        expected_date = '3/22/2007'
        actual_date = self.publication.get_date()

        self.assertEqual(actual_date, expected_date)


class USPTODataTests(TestCase):

    def test_normalize_date(self):
        not_normalized_date = 'May 1, 2008'
        expected_date = '5/1/2008'

        self.assertEqual(expected_date, USPTOExtractDateMixin().normalize_date(not_normalized_date))

class ForeignPublicationTests(TestCase):

    def test_normalize_date(self):
        not_normalized_date = '20060928'
        expected_date = '9/28/2006'

        self.assertEqual(expected_date, ForeignPublication._normalize_date(not_normalized_date))
