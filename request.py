import requests
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s', filename='process.log')
success=1
failed=0
def check_valid(url):
    response = requests.get(url['url'])
    requests.session().close()
    if response.status_code == 200:
        logging.info(f'response code success : {response.status_code}')
        return success
    else:
        logging.error(f'response failed with code : {response.status_code} , please try after sometime')
        return failed

def get_content(url):
    content = requests.get(url['url'])
    requests.session().close()
    return content.json()

