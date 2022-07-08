import requests
import json
import logging, os
## 利用GoogleMap Place API搜尋地點
## input 搜尋地點: str
## ouput { "PlaceName", "lat", "lon" }




def find_place(search_name):
    try:
        with open("Tokens.json", "r") as file:
            API_KEY = json.load(file).get("GoogleMap_API_Key")
    except FileNotFoundError:
        logging.warning("請先執行[第一次使用.exe]並輸入GoogleMap API KEY")
        os._exit(0)
    URL = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?language=zh-tw&input=" + search_name + "&inputtype=textquery&fields=name,geometry&key=" + API_KEY
    hearders = {}
    payload = {}
    response = requests.get(URL, headers=hearders, data=payload)
    place_data = response.json()
    if place_data.get("status") == "OK":
        StationName = place_data.get("candidates")[0].get("name")
        lat = place_data.get("candidates")[0].get("geometry").get("location").get("lat")
        lon = place_data.get("candidates")[0].get("geometry").get("location").get("lng")
        return {"StationName" : StationName, "lat" : lat, "lon" : lon}
    else:
        return None


def position(place):
    return { "lat" : place.get("candidates")[0].get("geometry").get("location").get("lat"),
            "lon" : place.get("candidates")[0].get("geometry").get("location").get("lng")}

if __name__ == "__main__":
    print(find_place("大安森林公園"))