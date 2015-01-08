__author__ = 'Eyal Fisher'

import os.path
from unittest import TestCase

from pairclient import PublicPairClient
from pairdata import PairApplication
from tsvparser import TsvParser


class FakePairClient():

    def fetch_application_zip(self, application_number):
        return '/home/eyal/Development/12900011.zip'


class PublicPairClientTests(TestCase):

    def test_file_is_downloaded(self):
        application_number = '12900011'

        client = PublicPairClient()
        file_location = client.fetch_application_zip(application_number)

        self.assertTrue(os.path.isfile(file_location))


class TestPairData(TestCase):

    def setUp(self):
        self.application = PairApplication('12900011', client=FakePairClient())

    def test_get_events(self):
        transactions = self.application.get_transactions()

        self.assertEqual(transactions[1]['date'], '04-13-2012')
        self.assertEqual(transactions[1]['description'], 'Email Notification')

    def test_get_first_named_inventor(self):
        inventor = self.application.get_first_named_inventor()

        self.assertEqual('David W. PARKINSON', inventor)

    def test_get_date(self):
        date = self.application.get_filing_date()

        self.assertEqual('10-07-2010', date)

    def test_get_examiner_name(self):
        examiner = self.application.get_examiner_name()

        self.assertEqual('FLEMING, FAYE M', examiner)

    def test_get_docket_number(self):
        docket_number = self.application.get_docket_number()

        self.assertEqual('AAI-70021', docket_number)

    def test_get_art(self):
        art = self.application.get_art()

        self.assertEqual('3616', art)

    def test_get_files(self):
        filepaths = self.application.get_files()
        self.assertEqual(len(filepaths), 50)


class TestTsvParser(TestCase):

    def test_tsv_parsed_correctly(self):
        parser = TsvParser()
        f = open('C:\\12900011-transaction_history.tsv', 'r')

        lines = list(parser.get_lines(f))

        self.assertEqual(lines[2][1], 'Email Notification')
