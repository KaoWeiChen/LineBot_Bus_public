import tkinter as tk
import json

def save():
    try:
        with open("Tokens.json", "r") as file:
            data = json.load(file)
        with open("Tokens.json", "w") as file:
            if CHANNEL_ACCESS_TOKEN_ent.get():
                data["CHANNEL_ACCESS_TOKEN"] = CHANNEL_ACCESS_TOKEN_ent.get()
            if CHANNEL_SECRET_ent.get():
                data["CHANNEL_SECRET"] = CHANNEL_SECRET_ent.get()
            if TDX_Client_ID_ent.get():
                data["TDX_Client_ID"] = TDX_Client_ID_ent.get()
            if TDX_Client_Secret_ent.get():
                data["TDX_Client_Secret"] = TDX_Client_Secret_ent.get()
            if GoogleMap_API_Key_ent.get():
                data["GoogleMap_API_Key"] = GoogleMap_API_Key_ent.get()
            json.dump(data, file, indent=4)


    except:
        data = {}
        with open("Tokens.json", "w") as file:
            if CHANNEL_ACCESS_TOKEN_ent:
                data["CHANNEL_ACCESS_TOKEN"] = CHANNEL_ACCESS_TOKEN_ent.get()
            if CHANNEL_SECRET_ent:
                data["CHANNEL_SECRET"] = CHANNEL_SECRET_ent.get()
            if TDX_Client_ID_ent:
                data["TDX_Client_ID"] = TDX_Client_ID_ent.get()
            if TDX_Client_Secret_ent:
                data["TDX_Client_Secret"] = TDX_Client_Secret_ent.get()
            if GoogleMap_API_Key_ent:
                data["GoogleMap_API_Key"] = GoogleMap_API_Key_ent.get()
            json.dump(data, file, indent=4)
    return

## 主視窗生成
win = tk.Tk()
win.title('輸入Token')
win.geometry("800x380")
win.resizable(False, False)

try:
    with open("Tokens.json", "r") as file:
        data = json.load(file)
except FileNotFoundError:
    data = {
        "CHANNEL_ACCESS_TOKEN" : None,
        "CHANNEL_SECRET" : None,
        "TDX_Client_ID" : None,
        "TDX_Client_Secret" : None,
        "GoogleMap_API_Key" : None,
    }
# Line
## CHANNEL ACCESS TOKEN
fm1 = tk.Frame(win)
fm1.pack(fill=tk.BOTH)
CHANNEL_ACCESS_TOKEN_text = tk.Label(fm1, fg='black', text='CHANNEL ACCESS TOKEN :', font=('微軟正黑體', 20), padx=10, pady=10)
CHANNEL_ACCESS_TOKEN_text.pack(side=tk.LEFT, padx=10)
CHANNEL_ACCESS_TOKEN_ent = tk.StringVar(value=data.get("CHANNEL_ACCESS_TOKEN"))
ent1 = tk.Entry(fm1, width=52, justify='center', textvariable=CHANNEL_ACCESS_TOKEN_ent)
ent1.pack(side=tk.RIGHT, padx=17, pady=7, fill=tk.Y)

## CHANNEL SECRET
fm2 = tk.Frame(win)
fm2.pack(fill=tk.BOTH)
CHANNEL_SECRET_text = tk.Label(fm2, fg='black', text='CHANNEL SECRET :', font=('微軟正黑體', 20), padx=10, pady=10)
CHANNEL_SECRET_text.pack(side=tk.LEFT, padx=10)
CHANNEL_SECRET_ent = tk.StringVar(value=data.get("CHANNEL_SECRET"))
ent2 = tk.Entry(fm2, width=52, justify='center', textvariable=CHANNEL_SECRET_ent)
ent2.pack(side=tk.RIGHT, padx=17, pady=7, fill=tk.Y)

# TDX
## TDX Client ID
fm3 = tk.Frame(win)
fm3.pack(fill=tk.BOTH)
TDX_Client_ID_text = tk.Label(fm3, fg='black', text='TDX Client ID :', font=('微軟正黑體', 20), padx=10, pady=10)
TDX_Client_ID_text.pack(side=tk.LEFT, padx=10)
TDX_Client_ID_ent = tk.StringVar(value=data.get("TDX_Client_ID"))
ent3 = tk.Entry(fm3, width=52, justify='center', textvariable=TDX_Client_ID_ent)
ent3.pack(side=tk.RIGHT, padx=17, pady=7, fill=tk.Y)

## TDX Client Secret
fm4 = tk.Frame(win)
fm4.pack(fill=tk.BOTH)
TDX_Client_Secret_text = tk.Label(fm4, fg='black', text='TDX Client Secret :', font=('微軟正黑體', 20), padx=10, pady=10)
TDX_Client_Secret_text.pack(side=tk.LEFT, padx=10)
TDX_Client_Secret_ent = tk.StringVar(value=data.get("TDX_Client_Secret"))
ent4 = tk.Entry(fm4, width=52, justify='center', textvariable=TDX_Client_Secret_ent)
ent4.pack(side=tk.RIGHT, padx=17, pady=7, fill=tk.Y)

# GoogleMap
fm5 = tk.Frame(win)
fm5.pack(fill=tk.BOTH)
GoogleMap_API_Key_text = tk.Label(fm5, fg='black', text='GoogleMap API Key :', font=('微軟正黑體', 20), padx=10, pady=10)
GoogleMap_API_Key_text.pack(side=tk.LEFT, padx=10)
GoogleMap_API_Key_ent = tk.StringVar(value=data.get("GoogleMap_API_Key"))
ent5 = tk.Entry(fm5, width=52, justify='center', textvariable=GoogleMap_API_Key_ent)
ent5.pack(side=tk.RIGHT, padx=17, pady=7, fill=tk.Y)

# 儲存
fm6 = tk.Frame(win)
fm6.pack(fill=tk.BOTH)

btnsave = tk.StringVar()
btnsave.set("儲存")
btn = tk.Button(fm6, bg='#71C973', fg='white', textvariable=btnsave,  font=('微軟正黑體', 20), command=save, pady=10)
btn.pack(side=tk.BOTTOM)


win.mainloop()