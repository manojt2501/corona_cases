import requests
import logging


# function to get content from URL
def get_content(url):
    result = requests.get(url['url'])
    requests.session().close()
    if result.status_code == 200:
        logging.info(f'response code success : {result.status_code}')
        return result.json()
    else:
        logging.error(f'response failed with code : {result.status_code} , please try after sometime')
        return False
