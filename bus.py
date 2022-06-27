from base64 import decode
import requests
import time
import json

TDX_URL = 'https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token'
client_id = "40540129s-6b8a80eb-2f93-4627"
client_secret = "4b3e8ace-d4cc-4df3-a644-367681ba1066"


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
    

###1.  傳入[start_stop]、[end_stop]
def find_bus(start_stop: str, end_stop: str, token: str):   

### 2.  從station_info找到[start_stop]中[All_RouteID]          
    with open("Station_info.json") as file:
        station = json.load(file)
    StationRoute = None
    for i in station:
        if i.get("StationName").get("Zh_tw") == start_stop:
            StationRoute = i.get("Stops")
            break
    if not StationRoute:
        return "起始公車站輸入錯誤!"
    All_RouteID = []
    for Route in StationRoute:
        All_RouteID.append(Route.get("RouteName").get("Zh_tw"))

### 3.從[ALL_RouteID]中找出所有可以抵達[end_stop]的[RouteID]
    reachable = []
    for route in All_RouteID:
        pass



def testTokenAvailable(token):
    pass




def main():
    tdx_token = get_token()
    if not tdx_token:
        print("取得Token失敗")
        return
    else:
        print("token = {}".format(tdx_token))
    URL = "https://tdx.transportdata.tw/api/basic/v2/Bus/Stop/City/Taipei"
    header = {"authorization" : "Bearer " + tdx_token}
    payload = {"format" : "JSON"}
    response = requests.get(URL, headers=header, params=payload)
    response_text = response.text
    print("status code = {}".format(response.status_code))
    data = json.loads(response_text)
    with open("Stop_info.json", mode = "w", encoding = "utf-8") as file:
        file.write(str(data))
    return

    


if __name__ == "__main__":
    main()
