import requests
import csv
response = requests.get("https://api.covid19api.com/summary")
data=response.json()
corona_cases=data['Countries']
for i in corona_cases:
    del i['Slug']
    del i['Premium']
    del i['ID']
with open('country_corona.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=['Country','CountryCode','NewConfirmed','TotalConfirmed','NewDeaths','TotalDeaths','NewRecovered','TotalRecovered','Date'])
    writer.writeheader()
    for list in corona_cases:
        writer.writerow(list)
    csvfile.close()



# print(corona_cases)

