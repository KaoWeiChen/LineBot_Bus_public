import requests
import time
import json
import math
import ijson

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
    

###1.  傳入[start_stop : str]、[end_stop : str]
def find_bus(start_stop: str, end_stop: str, token: str):   

### 2.  從station_info找到[start_stop]中[All_RouteID]          
    with open("Station_info.json", "rb") as file:
        StationRoute = None
        for station in ijson.items(file, "item"):
            if station.get("StationName").get("Zh_tw") == start_stop:
                StationRoute = station.get("Stops")
                StartID = station.get("StationID")
                break
    if not StationRoute:
        return "起始公車站輸入錯誤!"
    All_RouteID = []
    for Route in StationRoute:
        All_RouteID.append(Route.get("RouteName").get("Zh_tw"))

### 3.從[ALL_RouteID]中找出所有可以抵達[end_stop]的[RouteID, direction]
    reachable = []
    request_times = 0
    for route in All_RouteID:
        # API呼叫次數 50次/秒
        if request_times >=50:
            request_times = 0
            time.sleep(1)
        request_times+=1
        direction = isReachable(route, start_stop, end_stop, token)
        if direction >= 0:
            reachable.append([route, direction])
    if len(reachable) < 1:
        return "找不到從 {} 到 {} 的公車".format(start_stop, end_stop)

### 4.用[StartStopID]找到所有將要到達的公車，並取出[reachable]的到達時間
    comming = reach_StartStop_time(reachable, StartID, token)
    if len(comming) < 1:
        return "目前沒有 從 {} 到 {} 的班車".format(start_stop, end_stop)
    message = ""
    for route in comming:
        message+= "{} 將在 {}後抵達 {} \n".format(route, transSec(comming.get(route)), start_stop)
    return message

        

# 查詢route是否可從start_stop到達end_stop，若可以回傳direction，否則回傳-1
def isReachable(route: str, start_stop: str, end_stop: str, token) -> int:
        Route_URL = "https://tdx.transportdata.tw/api/basic/v2/Bus/DisplayStopOfRoute/City/Taipei/" + route
        header = {"authorization" : "Bearer " + token}
        payload = {"format" : "JSON"}
        Route_response = requests.get(Route_URL, headers = header, params=payload)
        StopOfRoute = json.loads(Route_response.text)
        StartFound = 0
        for direction in range(len(StopOfRoute)):
            for stop in StopOfRoute[direction].get("Stops"):
                if start_stop == stop.get("StopName").get("Zh_tw"):
                    StartFound = 1
                if end_stop == stop.get("StopName").get("Zh_tw") and StartFound == 1:
                    return direction
        return -1

def reach_StartStop_time(routes, StartID, token):
    CommingBus_URL = "https://tdx.transportdata.tw/api/advanced/v2/Bus/EstimatedTimeOfArrival/City/Taipei/PassThrough/Station/" + StartID
    header = {"authorization" : "Bearer " + token}
    payload = {"format" : "JSON"}
    CommingBus_response = requests.get(CommingBus_URL, headers= header, params= payload)
    comming_bus = json.loads(CommingBus_response.text)
    comming = {}
    for bus in comming_bus:
        for route in routes:
            if bus.get("RouteName").get("Zh_tw") == route[0] and bus.get("Direction") == route[1]:
                if not bus.get("EstimateTime"):
                    continue
                if route[0] not in comming:
                    comming[route[0]] = bus.get("EstimateTime")
                else:
                    if bus.get("EstimateTime") < comming.get(route[0]):
                        comming[route[0]] = bus.get("EstimatieTime")
    return comming


def testTokenAvailable(token):
    pass

def transSec(sec):
    minute = math.floor(sec/60)
    sec = sec%60
    return "{} 分 {}秒".format(minute, sec)


def main():
    start = time.time()
    tdx_token = get_token()
    if not tdx_token:
        print("取得Token失敗")
        return
    else:
        print("取得Token成功")
    print(find_bus("師大分部", "臺大", tdx_token))
    end = time.time()
    print("執行時間 : {}秒".format(end-start))

    


if __name__ == "__main__":
    main()
