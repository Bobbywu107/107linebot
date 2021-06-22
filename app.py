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
    elif event.message.text == "中翻韓":
        msg =  TextSendMessage(text = '語言設定為韓文')
        lang='ko'
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
                    image_url="https://im.marieclaire.com.tw/m800c533h100b0/assets/mc/201904/5CC85BAE267B41556634542.jpeg",
                    action=URITemplateAction(
                        label="K-BOY",
                        uri="https://im.marieclaire.com.tw/m800c533h100b0/assets/mc/201904/5CC85BAE267B41556634542.jpegh"
                    )
                ),
                ImageCarouselColumn(
                    image_url="https://news.agentm.tw/wp-content/uploads/cover-1-1258-750x422.jpg",
                    action=URITemplateAction(
                        label="K-BOY-2",
                        uri="https://news.agentm.tw/wp-content/uploads/cover-1-1258-750x422.jpg"
                    )
                ),
                
                ImageCarouselColumn(
                    image_url="https://scontent.fkhh1-1.fna.fbcdn.net/v/t1.6435-0/c0.0.768.768a/s552x414/198324618_2497430827068812_1586733109475507562_n.jpg?_nc_cat=100&ccb=1-3&_nc_sid=da31f3&_nc_ohc=jNT4cjqsXPwAX_hT_nw&_nc_ht=scontent.fkhh1-1.fna&tp=28&oh=81fa886168aad03743aac20ab49ce930&oe=60D621CF",
                    action=URITemplateAction(
                        label="K-BOY-3",
                        uri="https://scontent.fkhh1-1.fna.fbcdn.net/v/t1.6435-0/c0.0.768.768a/s552x414/198324618_2497430827068812_1586733109475507562_n.jpg?_nc_cat=100&ccb=1-3&_nc_sid=da31f3&_nc_ohc=jNT4cjqsXPwAX_hT_nw&_nc_ht=scontent.fkhh1-1.fna&tp=28&oh=81fa886168aad03743aac20ab49ce930&oe=60D621CF"
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
    