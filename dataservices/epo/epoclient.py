__author__ = 'Eyal Fisher'

import requests
import base64


class RegisteredClient:
    def __init__(self, consumer_key, consumer_secret):
        self.authentication_url = 'https://ops.epo.org/3.1/auth/accesstoken'
        self.access_token = ''
        self.authenticate(consumer_key, consumer_secret)

    def authenticate(self, consumer_key, consumer_secret):
        base64_authentication = base64.b64encode(':'.join([consumer_key, consumer_secret]))

        payload = 'grant_type=client_credentials'
        headers = {
            'Authorization': 'Basic ' + base64_authentication,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.post(self.authentication_url, data=payload, headers=headers)
        response.raise_for_status()

        self.access_token = response.json()['access_token']

    def fetch_publication_xml(self, epo_publication_reference):
        fetching_url = 'https://ops.epo.org/3.1/rest-services/published-data/search/abstract,biblio,full-cycle/'

        headers = self._get_access_token_header()

        response_data = requests.get(fetching_url, params={'q': epo_publication_reference}, headers=headers)
        response_data.raise_for_status()

        return response_data

    def fetch_publication_xml_by_publication_reference(self, reference_number):
        fetching_url = 'http://ops.epo.org/3.1/rest-services/published-data/publication/epodoc/%s/full-cycle' % (reference_number,)

        headers = self._get_access_token_header()

        response_data = requests.get(fetching_url, headers=headers)
        response_data.raise_for_status()

        return response_data


    def fetch_applicant_xml(self, applicant_name, first_index, last_index):
        fetching_url = 'https://ops.epo.org/3.1/rest-services/published-data/search/full-cycle/'
        query = 'applicant = "{0}"'.format(applicant_name)

        headers = self._get_access_token_header()

        range_parameter = '{0}-{1}'.format(first_index, last_index)
        response_data = requests.get(fetching_url, params={'q': query, 'range': range_parameter}, headers=headers)
        response_data.raise_for_status()

        return response_data

    def fetch_events_xml_by_reference_number(self, reference_number):
        fetching_url = 'https://ops.epo.org/3.1/rest-services/register/publication/epodoc/%s/events' \
                       % (reference_number,)

        return self._simple_get_with_headers(fetching_url)

    def fetch_image_information_xml(self, epo_doc_publication_number):
        fetching_url = 'http://ops.epo.org/rest-services/published-data/publication/epodoc/%s/images' \
                       % (epo_doc_publication_number,)

        return self._simple_get_with_headers(fetching_url)

    def _simple_get_with_headers(self, url):
        headers = self._get_access_token_header()

        response_data = requests.get(url, headers=headers)
        response_data.raise_for_status()

        return response_data

    def _get_access_token_header(self):
        headers = {
            'Authorization': 'Bearer ' + self.access_token
        }

        return headers

