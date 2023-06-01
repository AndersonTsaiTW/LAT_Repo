from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,ImageMessage
)
import os
import string
import chatgptENG
import brtestpr1
import local_bread
local_port = 3001

app = Flask(__name__)

line_bot_api = LineBotApi('23uRE8qB1LbXm8pngifTyRsCVqzW6voA1XPT7hPkHkPbjVqwv6mEB0yERdS272A0gTVLO+78v/13izdnyxkmETscJbqy8HwcfuLD4DJQkHn9xzKH69eSNmelW2ssiOm21Ez+L+5SdZd/O4xRcycNnQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('d1793208aa7e0d0716a1a4d90a04dbff')
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=(ImageMessage,TextMessage))
def handle_message(event):
    if isinstance(event.message, TextMessage):
        if event.message.text == "你好":
            buttons_template = TemplateSendMessage(
                alt_text='啟動服務',
                template=ButtonsTemplate(
                    title='你想選擇哪種圖像辨識的服務呢?',
                    text='請選擇',
                    thumbnail_image_url='https://i.imgur.com/gt4Ke6o.jpg',
                    actions=[
                        MessageTemplateAction(
                            label='傳送圖片',
                            text='傳送圖片'
                        ),
                        MessageTemplateAction(
                            label='傳送網址',
                            text='傳送網址'
                        )
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token, buttons_template)

        elif event.message.text == "傳送圖片":
            content = "請給我一張你想要知道的麵包圖片吧!"
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=content))

        elif event.message.text == "傳送網址":
            content = "請給我一個你想要知道的麵包網址吧!"
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=content))

        else:
            image_url = event.message.text
            breadtag = brtestpr1.breadpredict(image_url)
            reply_text = chatgptENG.chatgptfn(breadtag)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=reply_text.choices[0].message.content))

    elif isinstance(event.message, ImageMessage):
        ext = 'jpg'
        image_content = line_bot_api.get_message_content(event.message.id)
        directory = './static/'
        existing_images = len(os.listdir(directory))
        next_image_number = existing_images + 1
        image_number_str = str(next_image_number).zfill(4)
        image_name = image_number_str + '.jpg'
        path = directory + image_name

        with open(path, 'wb') as fd:
            for chunk in image_content.iter_content():
                fd.write(chunk)
        directory = './static/'
        existing_images = len(os.listdir(directory))
        image_number_str = str(existing_images).zfill(4)
        image_name = image_number_str + '.jpg'
        image_url = os.path.join(directory, image_name)
        breadtag = local_bread.breadpredict(image_url)
        reply_text = chatgptENG.chatgptfn(breadtag)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text.choices[0].message.content))


if __name__ == "__main__":
    app.run(port=local_port)