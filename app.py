from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('0/dp7Yz2hk1/9CImY8JLS0ZZtr4EtswvZ9voUSkln2iZUOGDkKygXJtPt1j0toWfwLu/2ImT8WVywQcHGZkQGYmxz3aBD3Unm+UYwcAlRMyKRnTkFfQ5DLBnGKPvO6EufSIbbolTvGh+5llp9QkcTAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('d74f34387daad07c7ec2fb7423eecda1')


# 監聽所有來自 /callback 的 Post Request
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

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    text=event.message.text

    if (text=="Hi"):
        reply_text = "Hello"
    elif(text=="你好"):
        reply_text = "哈囉"
    elif(text=="機器人"):
        reply_text = "叫我嗎"
    elif(text=="誒"):
        reply_text = "幹嘛"
    else:
        reply_text = text
#如果非以上的選項，就會學你說話

    message = TextSendMessage(reply_text)
    line_bot_api.reply_message(event.reply_token, message)

   

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    