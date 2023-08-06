API_URL = 'https://manhattan-api-rijk2jvapq-ue.a.run.app/'
EQUITIES_PUBLIC_API_KEY = "-----BEGIN EQUITIES PACKAGE POLITY PUBLIC KEY-----MIIEogIBAAKCAQB+HzZs3fL2vx8l2qnu9z0QhurriGU0vvSJbro2AHuQeBdYbQSC-----END EQUITIES PACKAGE POLITY PUBLIC KEY-----"

DATASET_NAME_DESC_QUERY = '''
    query {
        datasets{
            name
            desc
        }
    }'''

COMPANY_CIK_NAME_QUERY = '''
    query {
        companies{
            cik
            name
        }
    }'''

DATASET_QUERY = lambda name, api_key : '''
    query {
        dataset(name:"%s","%s"){
            name
            source
            desc
            years
            results
        }
    }'''%(name,api_key)

COMPANY_QUERY = lambda cik, api_key : '''
    query {
        company(cik:"%s",apiKey : "%s"){
            income
            cash
            balance
        }
    }'''%(cik,api_key)

FINANCIAL_STATEMENT_QUERY = lambda cik, kind, api_key :'''
    query {
        company(cik:"%s",apiKey:"%s"){
            %s
        }
    }'''%(cik,api_key,kind)

def take_a_sec():
    print('  - this could take a sec...')

def initialize():
    print('> 🏛️\twelcome to polity.')

def initialized():
    print('> 🌟\tauth success. apis connected')

def failed():
    print('> ☠️\tclient failed to connect to api!')

def datasets():
    print('> 🛰️\tretrieving datasets ...')

def dataset(name):
    print('> 📦\tfetching dataset: %s ...'%name)

def companies():
    print('>🛰️\tretrieving company ciks ...')

def company(cik):
    print('>📦\tfetching company: %s ...'%cik)
    
def financial_statement(name,kind):
    print('> 📦\tfetching financial statement: %s for %s ...'%(kind,kind))
