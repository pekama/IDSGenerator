__author__ = 'eyal'

from unittest import TestCase
from dataservices.uspto.USPTOdata import USPTOPatent, USPTOClient, USPTOPublication, ForeignPublication


class USPTOPatentTests(TestCase):

    def setUp(self):
        self.patent = USPTOPatent('7532932')
        self.patent2 = USPTOPatent('5861019')

    def test_get_inventor(self):
        self.assertEqual(self.patent.get_inventor(), 'Denker et al.')
        self.assertEqual(self.patent2.get_inventor(), 'Sun et al.')

    def test_get_dates(self):
        self.assertEqual(self.patent.get_date(), '5/12/2009')
        self.assertEqual(self.patent2.get_date(), '1/19/1999')


class USPTOPublicationTests(TestCase):

    def setUp(self):
        self.publication = USPTOPublication('20070067007')
        self.publication2 = USPTOPublication('20080103407')

    def test_get_applicant(self):
        self.assertEqual(self.publication.get_applicant(), 'Schulman Joseph H. et al.')
        self.assertEqual(self.publication2.get_applicant(), 'Bolea Stephen L. et al.')

    def test_get_date(self):
        self.assertEqual(self.publication.get_date(), '3/22/2007')
        self.assertEqual(self.publication2.get_date(), '5/1/2008')


class ForeignPublicationTests(TestCase):

    def setUp(self):
        self.publication = ForeignPublication('WO2006102626')
        self.publication2 = ForeignPublication('WO2012012591')

    def test_get_applicant(self):
        self.assertEqual(self.publication.get_applicant(), 'METACURE NV [NL]')
        self.assertEqual(self.publication2.get_applicant(), 'RAFAEL DEV CORP LTD [IL]')

    def test_get_date(self):
        self.assertEqual(self.publication.get_date(), '9/28/2006')
        self.assertEqual(self.publication2.get_date(), '1/26/2012')