from gql import gql 

def query_dataset(client,name):
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
    '''%name
    query = gql(query)
    dataset = client.execute(query)['dataset']
    return dataset[0]
