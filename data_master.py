import logging
import configparser


# function to pop out unwanted tags from JSON
def daily_cases(response_data):
    country_data = response_data['Countries']
    logging.info(f'API fetched {len(country_data)} countries data')
    for i in country_data:
        del i['Slug']
        del i['Premium']
        del i['ID']
    return country_data


# function to return last updated date from API for comparison purpose
def date_compare(res_data):
    api_temp_date = res_data['Global']['Date']
    api_date = api_temp_date[0: api_temp_date.index("T")]
    return api_date


# function to get values from ini file
def data_config(section):
    config = configparser.ConfigParser()
    config.read(r"D:\code\corona_cases\connection.ini")
    sql_string = dict(config.items('SQL'))
    url = dict(config.items('API'))
    result = 0
    if section == 'sql':
        result = sql_string
    elif section == 'url':
        result = url
    else:
        logging.error('invalid input')
    return result


# function to check if any input given matches with not_allowed list
def query_check(qry_input, not_allowed):
    qry_chk = any(item in qry_input for item in not_allowed)
    return qry_chk
