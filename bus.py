import requests
import time
import json
import math
import ijson
from find_place import (find_place, position)
import logging
import os

## find_bus: 輸入起、終點公車站名來找到可以搭乘的路線，並取得該路線到達起點公車站剩餘時間
## find_bus_positino: 輸入起、終點來搜尋兩點附近的公車站，並取得可以搭乘的路線與到達起點公車站剩餘時間

TDX_URL = 'https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token'

def get_token():
    try:
        with open("Tokens.json", "r") as file:
            data = json.load(file)
            tdx_client_id = data.get("TDX_Client_ID", None)
            tdx_client_secret = data.get("TDX_Client_Secret", None)        
    except FileNotFoundError:
        logging.warning("請先執行[第一次使用.exe]並輸入TDX資料")
        os._exit(0)
    times = 0
    header = {'content-type' : "application/x-www-form-urlencoded"}
    data = {"grant_type" : "client_credentials", "client_id" : tdx_client_id, "client_secret" : tdx_client_secret}
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

        
def find_bus_position(start: str, end: str, token :str, line_client_id = None):
    ## 當沒有經由line_bot呼叫此funcion時，自動升成一個client_id當作後面暫存檔名使用
    if not line_client_id:
        import random
        line_client_id = random.getrandbits(128)
    ## 利用google map搜尋該位置的經緯度
    start_place = find_place(start)
    end_place = find_place(end)
    if not start_place:
        return "起始位置輸入錯誤"
    elif not end_place:
        return "終點位置輸入錯誤"
    ## 搜尋起終點附近有無公車站
    start_station = position_get_station(start_place, token, "start", line_client_id)
    end_station = position_get_station(end_place, token, "end", line_client_id)
    if not start_station:
        return "起始位置附近沒有車站"
    if not end_station:
        return "終點附近沒有車站"

    with open("./Temp_Stations/start_{}.json".format(line_client_id), "r") as file:
        maxNum_of_start_stations_in_Temp = len(json.load(file))
    with open("./Temp_Stations/end_{}.json".format(line_client_id), "r") as file:
        maxNum_of_end_stations_in_Temp = len(json.load(file))
    for start_station_in_Temp in range(maxNum_of_start_stations_in_Temp):
        for end_station_in_Temp in range(maxNum_of_end_stations_in_Temp):
            start_station = readTempfile("start_{}.json".format(line_client_id), start_station_in_Temp)
            end_station = readTempfile("end_{}.json".format(line_client_id), end_station_in_Temp)
        ### 從[start_station[Stops]]中找出所有可以抵達[end_station]的[RouteID, direction]，並加入reachable
            start_routes = []
            end_routes = []
            for route in start_station.get("Stops"):
                start_routes.append(route.get("RouteName").get("Zh_tw"))
            for route in end_station.get("Stops"):
                end_routes.append(route.get("RouteName").get("Zh_tw"))
            reachable = []
            for route in start_routes:
                if route in end_routes:
                    reachable.append([route, Direction_Of_StartToEnd(route, start_station.get("StationName"), end_station.get("StationName"), token)])
            if len(reachable) < 1 :
                continue

        ### 從[Start_StationID]找到所有將要到達的公車，並取出[reachable]的到達時間
            comming = reach_StartStop_time(reachable, start_station.get("StationID"), token)
            if len(comming) < 1:
                continue
            message = "請到 {}站 搭乘公車到 {}站\n".format(start_station.get("StationName"), end_station.get("StationName"))
            for route in comming:
                message+= "{} 將在 {}後抵達 \n".format(route, transSec(comming.get(route)))
            ##  清除本次存取temp_station資料    
            open("./Temp_Stations/start_{}.json".format(line_client_id), "w").close()
            open("./Temp_Stations/end_{}.json".format(line_client_id), "w").close()
            return message
    ## 清除本次存取temp_station資料
    open("./Temp_Stations/start_{}.json".format(line_client_id), "w").close()
    open("./Temp_Stations/end_{}.json".format(line_client_id), "w").close()
    return "找不到 {} 到 {} 的公車".format(start, end)

    



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

### 取得[routes]到達某Station剩餘時間  
def reach_StartStop_time(routes, StationID, token):
    CommingBus_URL = "https://tdx.transportdata.tw/api/advanced/v2/Bus/EstimatedTimeOfArrival/City/Taipei/PassThrough/Station/" + StationID
    header = {"authorization" : "Bearer " + token}
    payload = {"format" : "JSON"}
    CommingBus_response = requests.get(CommingBus_URL, headers= header, params= payload)
    comming_bus = json.loads(CommingBus_response.text)
    comming = {}
    for bus in comming_bus:
        for route in routes:
            if bus.get("RouteName").get("Zh_tw") == route[0] and bus.get("Direction") == route[1]:
                if not bus.get("EstimateTime", None):
                    continue
                if route[0] not in comming:
                    comming[route[0]] = bus.get("EstimateTime")
                else:
                    if bus.get("EstimateTime") < comming.get(route[0]):
                        comming[route[0]] = bus.get("EstimatieTime")
    if len(comming) > 0:
        comming = { stop : arrivetime for stop, arrivetime in sorted(comming.items(), key=lambda item: item[1])}
    return comming

## 利用經緯度找到最近的5個station
def position_get_station(place, token, start_or_end, client_id):
    condition = True
    ratio = 100
    while condition:
        ratio+=100
        position_URL = "https://tdx.transportdata.tw/api/advanced/v2/Bus/Station/NearBy?$top=5&$spatialFilter=nearby({}, {}, {})&$format=JSON".format(place.get("lat"), place.get("lon"), ratio)
        header = {"authorization" : "Bearer " + token}
        payload = {}
        response = requests.get(position_URL, headers=header, params=payload)
        StationData = response.json()
        if len(StationData)>= 5 or ratio == 1000:
            if len(StationData) > 0:
                StationName0 = StationData[0].get("StationName").get("Zh_tw")
                Stops0 = StationData[0].get("Stops")
                StationID0 = StationData[0].get("StationID")
                WriteIn = []    ##  要寫入temp_stations的資料
                for i in range(len(StationData)):
                    WriteIn.append({"StationName" : StationData[i].get("StationName").get("Zh_tw"), "Stops" : StationData[i].get("Stops"), "StationID" : StationData[i].get("StationID")})
                with open("./Temp_Stations/{}_{}.json".format(start_or_end, client_id), "w", encoding="utf-8") as file:
                    json.dump(WriteIn, file, indent=4)
                return {"StationName" : StationName0, "Stops" : Stops0, "StationID" : StationID0}
            else:
                condition = False ## break while
        
    return None

## 找到[路線route]從[start_station]到[end_staiton]的Direction，若無法到達則回傳-1
def Direction_Of_StartToEnd(route, start_station_Name, end_station_Name, token):
    Route_URL = "https://tdx.transportdata.tw/api/basic/v2/Bus/DisplayStopOfRoute/City/Taipei/" + route
    header = {"authorization" : "Bearer " + token}
    payload = {"format" : "JSON"}
    Route_response = requests.get(Route_URL, headers=header, params=payload)
    StopOfRoute = json.loads(Route_response.text)
    StartFound = 0
    for direction in range(len(StopOfRoute)):
        for stop in StopOfRoute[direction].get("Stops"):
            if start_station_Name == stop.get("StopName").get("Zh_tw"):
                StartFound = 1
            if end_station_Name == stop.get("StopName").get("Zh_tw") and StartFound == 1:
                return direction
    return -1

def readTempfile(filename, order_of_station):
    with open("./Temp_Stations/"+filename, "r") as file:
        station = json.load(file)[order_of_station]
    return {"StationName" : station.get("StationName"), "Stops" : station.get("Stops"), "StationID" : station.get("StationID")}



def transSec(sec):
    minute = math.floor(sec/60)
    sec = sec%60
    return "{} 分 {}秒".format(minute, sec)

def testTokenAvailable(token):
    pass

def main():
    tdx_token = get_token()
    if not tdx_token:
        print("取得token失敗，請檢查TDX Client ID與TDX Client Secret是否正確")
        return
    ## find_bus( "出發公車站", "到達公車站", TDX_Token )
    print(find_bus("師大", "師大分部", tdx_token))

    ## find_bus_position( "出發地點", "到達地點", TDX_Token, "line client id": 使用line_bot時會自動傳入)
    print(find_bus_position("大安森林公園", "國家音樂廳", tdx_token, client_id="123"))

if __name__ == "__main__":
    main()
