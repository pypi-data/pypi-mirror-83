import json
import gql
import ast
from gql.transport.requests import RequestsHTTPTransport
import urllib3; urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import pandas as pd
from polity import static
from polity import schemas
from polity.static import (
    DATASET_NAME_DESC_QUERY,
    COMPANY_CIK_NAME_QUERY,
    FINANCIAL_STATEMENT_QUERY,
    DATASET_QUERY,
    COMPANY_QUERY,
    API_URL,
    EQUITIES_PUBLIC_API_KEY       
)

class Client():

    def __init__(self,api_key):

        static.initialize()

        self.api_url = API_URL
        self.api_key = api_key

        transport = RequestsHTTPTransport(
            url=self.api_url,
            use_json=True,
            headers={
                "Content-type": "application/json",
            },
            verify=False,
            retries=3,
        )

        self.graphql = gql.Client(
            transport=transport,
            fetch_schema_from_transport=True,
        )
        try:
            # authentication is attempted when grabbing metadata maps
            self.dataset_to_desc = self._fetch_dataset_to_desc_map()
            self.cik_to_name = self._fetch_cik_to_name_map()
            static.initialized()
        except:
            static.failed()
            pass

    def _fetch_dataset_to_desc_map(self):
        query = gql.gql(DATASET_NAME_DESC_QUERY)
        return {ds['name']:ds['desc'] for ds in 
            self.graphql.execute(query)['datasets']}

    def _fetch_cik_to_name_map(self):
        query = gql.gql(COMPANY_CIK_NAME_QUERY)
        return {c['cik']:c['name'] for c in 
            self.graphql.execute(query)['companies']}

    def dataset(self,name):
        static.dataset(name)
        query = gql.gql(DATASET_QUERY(name,self.api_key))
        return self.graphql.execute(query)['dataset'][0]

    def datasets(self):
        static.datasets()
        return list(self._fetch_dataset_to_desc_map().keys())

    def company(self,cik,df=False):
        
        def to_df(statement):
            statement_df = pd.DataFrame.from_dict(json.loads(statement))
            return statement_df.reindex(sorted(statement_df.columns),axis=1)

        static.company(cik)
        query = gql.gql(COMPANY_QUERY(cik,self.api_key))
        data = self.graphql.execute(query)['company'][0]

        if df: 
            if data['income']: data['income'] = to_df(data['income'])
            if data['balance']: data['balance'] = to_df(data['balance']) 
            if data['cash']: data['cash'] = to_df(data['cash'])
            if data['equity']: data['equity'] = to_df(data['equity'])
        return schemas.company(data)

    def companies(self):
        static.companies()
        return list(self._fetch_cik_to_name_map().keys())

    def ciks(self): return self.companies()

    def financial_statement(self,cik,kind,df=False):
        static.financial_statement(self.cik_to_name[cik],kind)
        query = gql.gql(FINANCIAL_STATEMENT_QUERY(cik,kind,self.api_key))
        statement = self.graphql.execute(query)['company'][0][kind]
        statement = pd.DataFrame.from_dict(json.loads(statement))
        if df: return statement.reindex(sorted(statement.columns),axis=1)
        else: return statement
