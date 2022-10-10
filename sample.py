import api

def main(url):
    response = api.call_api(url)
    return response.text