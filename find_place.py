import requests

## 利用GoogleMap Place API搜尋地點
## input 搜尋地點: str
## ouput { "PlaceName", "lat", "lon"}

API_KEY = "AIzaSyCcErOJ-RtjuHFNDoN2KiyyL08AE-z72gM"

def find_place(search_name):
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
    print(find_place("台大"))