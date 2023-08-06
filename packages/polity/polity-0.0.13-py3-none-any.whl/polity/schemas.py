company = lambda data : {
    'name':data['name'],
    'sic':data['sic'],
    'business_address':
        {
            "country":data['countryba'],
            "city": data['cityba'],
            "zip": data['zipba'],
            "adr1": data['bas1'],
            "adr2": data['bas2'],
        },
    'mailing_address':
        {
            "country":data['countryma'],
            "city": data['cityma'],
            "zip": data['zipma'],
            "adr1": data['mas1'],
            "adr2": data['mas2'],
            "state": data['stprma']
        },
    'phone': data['baph'],
    'country_incorporated': data['countryinc'],
    'state_incorporated' : data['stprinc'],
    'ein' : data['ein'],
    'former_name': data['former'],
    'income':data['income'],
    'balance':data['balance'],
    'cash':data['cash'],
    'equity': data['equity']
}