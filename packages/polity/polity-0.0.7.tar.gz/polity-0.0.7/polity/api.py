import json
import gql
from gql.transport.requests import RequestsHTTPTransport

import pandas as pd
import ast

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

API_URL = 'https://manhattan-api-rijk2jvapq-ue.a.run.app/'

class Client():

    def __init__(self,api_key='DEV'):

        self.api_url = API_URL
        self.api_key = api_key

        self.DATASET_NAME_DESC_QUERY = '''
            query {
                datasets{
                    name
                    desc
                }
            }
        '''

        self.COMPANY_CIK_NAME_QUERY = '''
            query {
                companies{
                    cik
                    name
                }
            }
        '''

        self.DATASET_QUERY = lambda name : '''
            query {
                dataset(name:"%s"){
                    name
                    source
                    desc
                    years
                    results
                }
            }
        '''%name

        self.COMPANY_QUERY = lambda cik : '''
            query {
                company(cik:"%s"){
                    income
                    cash
                    balance
                }
            }
        '''%cik

        self.FINANCIAL_STATEMENT_QUERY = lambda cik,kind :'''
            query {
                company(cik:"%s"){
                    %s
                }
            }
        '''%(cik,kind)

        
        self._gql_transport=RequestsHTTPTransport(
            url=self.api_url,
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

    def _fetch_dataset_to_desc_map(self):
        query = gql.gql(self.DATASET_NAME_DESC_QUERY)
        results = self._gql_client.execute(query)
        return {ds['name']:ds['desc'] for ds in results['datasets']}

    def _fetch_cik_to_name_map(self):
        query = gql.gql(self.COMPANY_CIK_NAME_QUERY)
        results = self._gql_client.execute(query)
        return {c['cik']:c['name'] for c in results['companies']}

    def dataset(self,name):
        query = gql.gql(self.DATASET_QUERY(name))
        results = self._gql_client.execute(query)
        return results['dataset'][0]

    def datasets(self):
        return list(self._fetch_dataset_to_desc_map().keys())

    def company(self,cik):
        query = gql.gql(self.COMPANY_QUERY(cik))
        results = self._gql_client.execute(query)['company']
        return results[0]

    def companies(self):
        return list(self._fetch_cik_to_name_map().keys())

    def financial_statement(self,cik,kind,df=False):
        query = gql.gql(self.FINANCIAL_STATEMENT_QUERY(cik,kind))
        results = self._gql_client.execute(query)['company']
        
        statement = results[0][kind]
        if df:
            statement = json.loads(statement.replace('~','"'))
            return pd.DataFrame.from_dict(statement)
        else: return statement


if __name__ == '__main__':
    api = Client()

    for cik in api.companies():
        try:
            print(api.financial_statement(cik=cik,kind='cash',df=True))
        except:
            pass



