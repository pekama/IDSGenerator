__author__ = 'Eyal Fisher'

import urllib


class PublicPairClient:

    def __init__(self):
        self.base_url = 'http://patents.reedtech.com/downloads/pair/'

    def fetch_application_zip(self, application_number):
        file_location, headers = urllib.urlretrieve(
            url=self._get_fetch_url(application_number),
        )

        return file_location

    def _get_fetch_url(self, application_number):
        return '{0}/{1}.zip'.format(self.base_url, application_number)
