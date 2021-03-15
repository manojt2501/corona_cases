import csv
import content_data
def main():
    with open('country_corona.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['Country', 'CountryCode', 'NewConfirmed', 'TotalConfirmed', 'NewDeaths',
                                            'TotalDeaths', 'NewRecovered', 'TotalRecovered', 'Date'])
        writer.writeheader()
        daily_updates=content_data.daily_cases()
        print(daily_updates)
        for list in daily_updates:
            writer.writerow(list)
        csvfile.close()

if __name__=="__main__":
    main()

