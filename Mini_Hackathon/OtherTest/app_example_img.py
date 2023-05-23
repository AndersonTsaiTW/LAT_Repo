# app.py
# reference_1:https://www.youtube.com/watch?v=i8ncIcJs-LA&ab_channel=Maso%E7%9A%84%E8%90%AC%E4%BA%8B%E5%B1%8B
# reference_2:https://www.youtube.com/watch?v=uqkJmsb8UIY&ab_channel=Maso%E7%9A%84%E8%90%AC%E4%BA%8B%E5%B1%8B
# reference_3:https://ithelp.ithome.com.tw/users/20142564/articles
# reference_Flask:https://devs.tw/post/448


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

@handler.add(MessageEvent)
def handle_message(event):
    if (event.message.type == "image"):
        SendImage = line_bot_api.get_message_content(event.message.id)
        print(SendImage)

'''
ngrok_url = "https://6b59-118-165-9-211.ngrok-free.app"

@handler.add(MessageEvent)
def handle_message(event):
	if (event.message.type == "image"):
		SendImage = line_bot_api.get_message_content(event.message.id)

		local_save = './static/' + event.message.id + '.png'
		with open(local_save, 'wb') as fd:
			for chenk in SendImage.iter_content():
				fd.write(chenk)
                
		line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url = ngrok_url + "/static/" + event.message.id + ".png",preview_image_url = ngrok_url + "/static/" + event.message.id + ".png"))
'''

if __name__ == "__main__":
    app.run()