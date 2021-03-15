import requests
def get_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        print(f"Response successful: {response.status_code}")
        return response.json()
    else:
        print(f"Request completed with Error. Response Code : {response.status_code}")
        return None
