import requests

TDX_URL = 'https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token'
client_id = 1
client_secret = 1


def get_token(times):
    header = {'content-type' : "application/x-www-form-urlencoded"}
    data = {"grant_type" : "client_credentials", "client_id" : client_id, "client_secret" : client_secret}
    response = requests.post(TDX_URL, headers = header, data = data)
    if response.status_code == 200:
        return response.json().get("access_token")
    elif times<5:
        times+=1
        get_token(times)
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
