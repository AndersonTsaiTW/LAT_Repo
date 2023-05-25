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
import chatgptENG
import brtestpr1
import local_bread
# from django.conf.urls.static import static
# from django.conf import settings
#set the local port number
local_port = 3001

app = Flask(__name__)

line_bot_api = LineBotApi('k3CowvkvvyCvpDNIdK5YhgGmjjCzSQUkJtpT9ws7f4sHzCazokmxAnr5Asyx9Nh6LWYmeNnzTHATunFsY4j3EYi+Ig2n0h/USG8PYaM7zQ75iGyxLm6L9bsWcPuq1fglAQ6mwqF0XzQi8ahqnORPeAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('39eb7c44608310ae94a1258853b0322a')
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
        ext = 'jpg'
        # message_content = line_bot_api.get_message_content(event.message.id)
        # bread_img = img_identify(message_content)

        # image_name = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(4))
        image_content = line_bot_api.get_message_content(event.message.id)
        # image_name = image_name.upper() + '.jpg'
        # path = './static/' + image_name

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
    # if isinstance(event.message, TextMessage):
        # image_url = event.message.text

        # directory = './static/'
        # existing_images = len(os.listdir(directory))+1
        # image_number_str = str(existing_images).zfill(4)
        # image_name = image_number_str + '.jpg'
        # image_url = directory + image_name

        directory = './static/'
        existing_images = len(os.listdir(directory))
        image_number_str = str(existing_images).zfill(4)
        image_name = image_number_str + '.jpg'
        image_url = os.path.join(directory, image_name)

        # image_url = './static/0002.jpg'
        #use bread identify program to get bread tag
        # breadtag = brtestpr1.breadpredict(image_url)
        breadtag = local_bread.breadpredict(image_url)
        print(breadtag)
        #send bread tag to chatGPT to catch the chinese and english introduction
        reply_text = chatgptENG.chatgptfn(breadtag)
        print(reply_text)
        #use line bot to reply the chatGPT answer
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text.choices[0].message.content))
    #        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run(port=local_port)