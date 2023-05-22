# app.py
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

#import project seperate models
import chatgptENG
import brtestpr1

#set the local port number
local_port = 3001

app = Flask(__name__)

line_bot_api = LineBotApi('23uRE8qB1LbXm8pngifTyRsCVqzW6voA1XPT7hPkHkPbjVqwv6mEB0yERdS272A0gTVLO+78v/13izdnyxkmETscJbqy8HwcfuLD4DJQkHn9xzKH69eSNmelW2ssiOm21Ez+L+5SdZd/O4xRcycNnQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('d1793208aa7e0d0716a1a4d90a04dbff')

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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    image_url = event.message.text
    #use bread identify program to get bread tag
    breadtag = brtestpr1.breadpredict(image_url)
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