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