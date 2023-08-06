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
            name
            sic 
            countryba
            cityba
            zipba 
            bas1
            bas2
            baph
            countryma
            stprma
            cityma
            zipma
            mas1
            mas2
            countryinc
            stprinc
            ein
            former
            changed
            income
            cash
            balance
            equity
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
    print('> 🏛️\tWelcome to polity.')

def initialized():
    print('> ✨\tAuth success. apis connected.')

def failed():
    print('> ☠️\tClient failed to connect to api!')

def datasets():
    print('> 🛰️\tRetrieving datasets ...')

def dataset(name):
    print('> 📦\tFetching dataset: %s ...'%name)

def companies():
    print('> 🛰️\tRetrieving company ciks ...')

def company(cik):
    print('> 📦\tFetching company: %s ...'%cik)
    
def financial_statement(name,kind):
    print('> 📦\tFetching financial statement: %s for %s ...'%(kind,name))
