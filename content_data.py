import logging
def daily_cases(respose_data):
    countrywise_data = respose_data['Countries']
    logging.info(f'API fetched {len(countrywise_data)} countries data')
    for i in countrywise_data:
        del i['Slug']
        del i['Premium']
        del i['ID']
    return countrywise_data

def date_compare(res_data):
    Api_tempdate= res_data['Global']['Date']
    Api_date=Api_tempdate[ 0 : Api_tempdate.index("T")]
    return Api_date


