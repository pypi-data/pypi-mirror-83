import gql
from gql.transport.requests import RequestsHTTPTransport

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Client():

    def __init__(self):
        self.manhattan_api_url = 'https://manhattan-api-rijk2jvapq-ue.a.run.app/'

        self.dataset_names = [
            'age_and_sex',
            'educational_attainment',
            'employment_status',
            'fertility',
            'households_and_families',
            'marital_status',
            'movers_between_regions',
            'total_population',
            'veteran_status'
        ]

        self._gql_transport=RequestsHTTPTransport(
            url=self.manhattan_api_url,
            use_json=True,
            headers={
                "Content-type": "application/json",
            },
            verify=False,
            retries=3,
        )

        self._gql_client = gql.Client(
            transport=self._gql_transport,
            fetch_schema_from_transport=True,
        )

    def get(self,dataset):
        query = '''
            query {
                dataset(name:"%s"){
                    name
                    source
                    desc
                    years
                    results
                }
            }
        '''%dataset
        query = gql.gql(query)
        dataset = self._gql_client.execute(query)['dataset']
        return dataset[0]

if __name__ == '__main__':
    c = Client()
    for dataset in c.dataset_names:
        r = c.get(dataset)
        print(r['name'],r['years'])


