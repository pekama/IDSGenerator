__author__ = 'Eyal Fisher'

from pairclient import PublicPairClient
from zipfile import ZipFile
from tsvparser import TsvParser
import os
import csv


class PairApplication():

    def __init__(self, application_reference, client=PublicPairClient()):
        self.client = client
        self.filename = self.client.fetch_application_zip(application_reference)
        self.application = application_reference
        self.tsvparser = TsvParser()

    def __delete__(self, instance):
        os.remove(self.filename)

    def get_transactions(self):
        transaction_filename = '{0}/{1}-transaction_history.tsv'.format(self.application, self.application)
        transactions = []

        with ZipFile(self.filename, 'r') as application_zip:
            transaction_file = application_zip.open(transaction_filename, 'r')
            for line in self.tsvparser.get_lines(transaction_file)[1:]:
                if len(line) != 2:
                    continue

                transactions.append(
                    {
                        'date': line[0],
                        'description': line[1]
                    }
                )

        return transactions

    def get_application_data(self):
        application_data_filename = '{0}/{1}-application_data.tsv'.format(self.application, self.application)
        with ZipFile(self.filename, 'r') as application_zip:
            application_data_file = application_zip.open(application_data_filename, 'r')
            lines = self.tsvparser.get_lines(application_data_file)

        return lines

    def get_first_named_inventor(self):
        name = self.get_application_data()[8][1]
        return name.split(',')[0].strip()

    def get_filing_date(self):
        date = self.get_application_data()[1][1]

        return date

    def get_examiner_name(self):
        examiner = self.get_application_data()[3][1]

        return examiner

    def get_art(self):
        art = self.get_application_data()[4][1]

        return art

    def get_docket_number(self):
        docket_number = self.get_application_data()[6][1]

        return docket_number

    ## returns a list of file paths, its the users responsibility to do the cleanup!!
    def get_files(self):
        with ZipFile(self.filename, 'r') as application_zip:
            directory_name = '{0}-image_file_wrapper'.format(self.application)
            application_zip.extractall()
            files = os.listdir('{0}/{1}/{2}'.format(os.curdir, self.application, directory_name))

            filepaths = [os.path.abspath(f) for f in files]

            return filepaths
