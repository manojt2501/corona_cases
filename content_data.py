import request
def daily_cases():
    URL = "https://api.covid19api.com/summary"
    corona = request.get_content(URL)
    countrywise_data = corona['Countries']
    for i in countrywise_data:
        del i['Slug']
        del i['Premium']
        del i['ID']
    return countrywise_data




