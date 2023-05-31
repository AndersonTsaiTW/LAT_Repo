# app.py
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,ImageMessage
)
import os
import string
#import project seperate models
import chatgptENG_v2_record
import brtestpr1
import local_bread
# from django.conf.urls.static import static
# from django.conf import settings
#set the local port number
local_port = 3001

app = Flask(__name__)

line_bot_api = LineBotApi('23uRE8qB1LbXm8pngifTyRsCVqzW6voA1XPT7hPkHkPbjVqwv6mEB0yERdS272A0gTVLO+78v/13izdnyxkmETscJbqy8HwcfuLD4DJQkHn9xzKH69eSNmelW2ssiOm21Ez+L+5SdZd/O4xRcycNnQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('d1793208aa7e0d0716a1a4d90a04dbff')

static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')

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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=(ImageMessage,TextMessage))
def handle_message(event):
    if isinstance(event.message, ImageMessage):
        print("這是圖片")
        ext = 'jpg'
        image_content = line_bot_api.get_message_content(event.message.id)
        directory = './static/'

        # 取得目錄下已有的圖片數量
        existing_images = len(os.listdir(directory))
        # 生成下一個圖片的順序編號
        next_image_number = existing_images + 1
        # 格式化編號，補零至4位數
        image_number_str = str(next_image_number).zfill(4)
        # 生成圖片名稱
        image_name = image_number_str + '.jpg'
        # 完整的路徑
        path = directory + image_name

        with open(path, 'wb') as fd:
            for chunk in image_content.iter_content():
                fd.write(chunk)

        image_url = os.path.join(directory, image_name)

        breadtag = local_bread.breadpredict(image_url)
    
    else:
        print("這是網址")
        image_url = event.message.text
        #use bread identify program to get bread tag
        breadtag = brtestpr1.breadpredict(image_url)
        #send bread tag to chatGPT to catch the chinese and english introduction
    print(breadtag)
    #因為AZURE還沒修好，先直接賦值做測試
    breadtag = "white_bread"

    reply_text = chatgptENG_v2_record.chatgptfn(breadtag)
    print(reply_text)
    #use line bot to reply the chatGPT answer
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text))
    
    chatgptENG_v2_record.breadchatrecord(breadtag,reply_text,2)


if __name__ == "__main__":
    app.run(port=local_port)