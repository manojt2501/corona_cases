import logging
def daily_cases(respose_data):
    countrywise_data = respose_data['Countries']
    logging.info(f'API fetched {len(countrywise_data)} countries data')
    for i in countrywise_data:
        del i['Slug']
        del i['Premium']
        del i['ID']
    return countrywise_data





