
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import requests
from bus import get_token
import MyCommand
import json

app = Flask(__name__)

line_bot_api = LineBotApi('bVsN9aiFABaRpxQDFS0d/MNE5dwAeh2PaQPXFImWRSHv+g2b36lJMhlbTYWq6SxlTA3GCnWyvJhCna/kC1dVUflsMCSgxouZsaIbHhKC6sxdMYwnc7pMAQOu9zFaZn3T2Bzj1bYeuJhRyDABuLAJsQdB04t89/1O/w1cDnyilFU=')

handler = WebhookHandler('c578b2dc2387d24d5e9b971f7829d702')

line_bot_api.push_message('U30838abc49d28474a3acf875481f7f6b', TextSendMessage(text='使用方式:\n1. 公車站 [起始公車站名]到[終點公車站名]\n2. 地名 [起始地點]到[終點]\n\n可利用command查找可用指令'))



@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

 
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

 
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    # client_id = json.loads(event.message.text).get("source").get("userId")

    # # 取得tdx_token失敗
    # if tdx_token == None:
    #     line_bot_api.reply_message(event.reply_token,"取得tdx token 失敗")
    # text = event.message.text
    # message = TextSendMessage(MyCommand.cmd(text, tdx_token, client_id))

    line_bot_api.reply_message(event.reply_token,message)

import os
if __name__ == "__main__":
    tdx_token = get_token()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)