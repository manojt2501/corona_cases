import logging


def daily_cases(response_data):
    country_data = response_data['Countries']
    logging.info(f'API fetched {len(country_data)} countries data')
    for i in country_data:
        del i['Slug']
        del i['Premium']
        del i['ID']
    return country_data


def date_compare(res_data):
    api_temp_date = res_data['Global']['Date']
    api_date = api_temp_date[0: api_temp_date.index("T")]
    return api_date
