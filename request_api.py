import requests
import logging


# check if API providing proper response
def check_valid(url):
    response = requests.get(url['url'])
    requests.session().close()
    if response.status_code == 200:
        logging.info(f'response code success : {response.status_code}')
        return True
    else:
        logging.error(f'response failed with code : {response.status_code} , please try after sometime')
        return False


# function to get content from URL
def get_content(url):
    content = requests.get(url['url'])
    requests.session().close()
    return content.json()
