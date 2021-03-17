import request
import content_data
import data_import
def main():

    URL = "https://api.covid19api.com/summary"
    if request.check_valid(URL) != 0:
        corona = request.get_content(URL)
        daily_updates = content_data.daily_cases(corona)
        data_import.create_conn()
    else:
        return 0

if __name__=="__main__":
    main()

