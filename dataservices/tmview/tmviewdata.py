import requests


class TMViewClient():

    def __init__(self):
        self.results_url = 'https://www.tmdn.org/tmview/search-tmv'

    def search(self, query):
        query_params = self._get_query_params(query, 1)

        response = requests.get(url=self.results_url, params=query_params)
        response_json = response.json()

        response_rows = response_json['rows']
        pages = int(response_json['total'])
        number_of_records = int(response_json['records'])

        for page in range(1, pages + 1):
            query_params = self._get_query_params(query, page)
            response_json = requests.get(url=self.results_url, params=query_params).json()

            response_rows.extend(response_json['rows'])

        return response_rows

    def _get_query_params(self, query, page):
        query_params = {
            '_search': 'false',
            'nd': '',
            'rows': '100',
            'page': page,
            'sidx': 'tm',
            'q':query,
            'sord': 'asc',
            'fq': '[]',
            'pageSize': '100',
            'selectedRowRefNumber': 'null',
            'providerList': 'null',
            'expandedOffices': 'null'
        }

        return query_params


class TMViewData():

    def __init__(self):
        self.client = TMViewClient()

    def get_trademarks(self, query):
        response_rows = self.client.search(query)

        result_rows = []
        for row in response_rows:
            registration_date = row.get('RegistrationDate', '-')
            nice_class = row.get('nc', [])
            application_date = row.get('ad', '')

            result_rows.append(
                {
                    'trademark': row['tm'],
                    'office': row['oc'],
                    'application_number': row['an'],
                    'status': row['sc'],
                    'nice_classes': nice_class,
                    'applicant_name': row['ApplicantName'],
                    'application_date': application_date,
                    'type': row['ty'],
                    'registration_date': registration_date
                }
            )

        return result_rows