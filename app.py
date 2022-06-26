
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import requests
import bus

app = Flask(__name__)

line_bot_api = LineBotApi('bVsN9aiFABaRpxQDFS0d/MNE5dwAeh2PaQPXFImWRSHv+g2b36lJMhlbTYWq6SxlTA3GCnWyvJhCna/kC1dVUflsMCSgxouZsaIbHhKC6sxdMYwnc7pMAQOu9zFaZn3T2Bzj1bYeuJhRyDABuLAJsQdB04t89/1O/w1cDnyilFU=')

handler = WebhookHandler('c578b2dc2387d24d5e9b971f7829d702')

line_bot_api.push_message('U30838abc49d28474a3acf875481f7f6b', TextSendMessage(text='你可以開始了'))


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
    # message = TextSendMessage(text=event.message.text)

    purpose = event.message.text                        ########
    if not bus.testTokenAvailable(token):
        token = bus.get_token()
    message = bus.call_tdx_service(purpose, token)


    line_bot_api.reply_message(event.reply_token,message)

import os
if __name__ == "__main__":
    token = bus.get_token()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)