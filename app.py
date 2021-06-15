from flask import Flask, request, abort

from translate import Translator

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *


app = Flask(__name__)
#translator = Translator (from_lang='zh-Hant', to_lang='en')

lang='en'

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
    global lang
    if event.message.text == "中翻英":
        msg = TextSendMessage(text = '語言設定為英文') 
        lang = 'en'
    elif event.message.text == "中翻日":
        msg =  TextSendMessage(text = '語言設定為日文')
        lang='ja'
    elif event.message.text == "圖片秀":
        msg =  image_carousel_message1() 
    else:
        translator = Translator (from_lang='zh-Hant', to_lang=lang)
        msg =  TextSendMessage(text = translator.translate(event.message.text))     
    line_bot_api.reply_message(event.reply_token, msg)


def image_carousel_message1():
    message = TemplateSendMessage(
        alt_text='圖片旋轉木馬',
        template=ImageCarouselTemplate(
            columns=[
                ImageCarouselColumn(
                    image_url="https://www.nups.ntnu.edu.tw/upfiles/univ-expo/%E5%8D%97%E9%83%A8/%E9%AB%98%E9%9B%84%E5%B8%82/%E6%8A%80%E5%B0%88%E6%A0%A1%E9%99%A2/%E6%96%87%E8%97%BB/%E6%96%87%E8%97%BB-pic02.jpg",
                    action=URITemplateAction(
                        label="文藻校園-1",
                        uri="https://www.nups.ntnu.edu.tw/upfiles/univ-expo/%E5%8D%97%E9%83%A8/%E9%AB%98%E9%9B%84%E5%B8%82/%E6%8A%80%E5%B0%88%E6%A0%A1%E9%99%A2/%E6%96%87%E8%97%BB/%E6%96%87%E8%97%BB-pic02.jpg"
                    )
                ),
                ImageCarouselColumn(
                    image_url="https://www.nups.ntnu.edu.tw/upfiles/univ-expo/%E5%8D%97%E9%83%A8/%E9%AB%98%E9%9B%84%E5%B8%82/%E6%8A%80%E5%B0%88%E6%A0%A1%E9%99%A2/%E6%96%87%E8%97%BB/%E6%96%87%E8%97%BB-pic03.jpg",
                    action=URITemplateAction(
                        label="文藻校園-2",
                        uri="https://www.nups.ntnu.edu.tw/upfiles/univ-expo/%E5%8D%97%E9%83%A8/%E9%AB%98%E9%9B%84%E5%B8%82/%E6%8A%80%E5%B0%88%E6%A0%A1%E9%99%A2/%E6%96%87%E8%97%BB/%E6%96%87%E8%97%BB-pic03.jpg"
                    )
                ),
                
                ImageCarouselColumn(
                    image_url="https://www.nups.ntnu.edu.tw/upfiles/univ-expo/%E5%8D%97%E9%83%A8/%E9%AB%98%E9%9B%84%E5%B8%82/%E6%8A%80%E5%B0%88%E6%A0%A1%E9%99%A2/%E6%96%87%E8%97%BB/%E6%96%87%E8%97%BB-pic04.jpg",
                    action=URITemplateAction(
                        label="文藻校園-3",
                        uri="https://www.nups.ntnu.edu.tw/upfiles/univ-expo/%E5%8D%97%E9%83%A8/%E9%AB%98%E9%9B%84%E5%B8%82/%E6%8A%80%E5%B0%88%E6%A0%A1%E9%99%A2/%E6%96%87%E8%97%BB/%E6%96%87%E8%97%BB-pic04.jpg"
                    )
                )
            ]
        )
    )
    return message

# requirements.txt 中要加入 translate , 也就是要 pip install traslate
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    