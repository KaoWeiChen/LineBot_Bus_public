import requests
import time
TDX_URL = 'https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token'
client_id = 1
client_secret = 1


def get_token():
    times = 0
    header = {'content-type' : "application/x-www-form-urlencoded"}
    data = {"grant_type" : "client_credentials", "client_id" : client_id, "client_secret" : client_secret}
    response = requests.post(TDX_URL, headers = header, data = data)
    while response.status_code != 200 and times < 5:
        time.sleep(0.1)
        response = requests.post(TDX_URL, headers = header, data = data)
        times+=1
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        return None
    


def call_tdx_service(purpose, token):
    url = apiToURL(purpose)
    header = {"authorization" : "Bearer " + token}
    response = requests.get(url, headers=header)


def testTokenAvailable(token):
    pass

def apiToURL(purpose):
    pass
