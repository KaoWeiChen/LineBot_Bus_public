# Line_Bus
#### 本專案是透過TDX運輸資料流通服務平台查詢台北市公車線路抵達站點時間，且可透過Line Bot機器人服務呼叫查詢功能
※本服務僅限於台北市地區\
※使用pipenv套件管理工具
* 使用到的套件有
  * requests
  * line-bot-sdk
  * flask
  * ijson
* 事前準備
  * TDX運輸資料流通服務平台申請會員取得API金鑰https://tdx.transportdata.tw/
  * Google Map地圖平台申請API https://developers.google.com/maps/ ( 需用到Places API功能 )
  * 若要透過Line Bot呼叫查詢功能，則需先建立Messaging API channel並完成各項設定
  
* 使用方式
  * 開啟第一次執行.exe輸入事前準備的資料
  * 執行MyCommand.py，依據格式選取查詢方式與要查詢的資料


* 成果範例:
> 1. Line加入LineBot_Bus機器人https://lin.ee/NUSDpJu
  
  ![image](https://github.com/Osalamia/LineBot_Bus_public/blob/main_public/L_gainfriends_qr.png)
  
> 2. 根據需求輸入指令

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(1) 公車站 [出發公車站名]到[到達公車站名] : 輸入起、終點公車站名來找到可以搭乘的路線，並取得該路線到達起點公車站剩餘時間

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(2) 地點 [出發地點]到[到達地點] : 輸入起、終點來搜尋兩點附近的公車站，並取得可以搭乘的路線與到達起點公車站剩餘時間

 ![image](https://github.com/Osalamia/LineBot_Bus_public/blob/main_public/%E7%AF%84%E4%BE%8B.jpg)
