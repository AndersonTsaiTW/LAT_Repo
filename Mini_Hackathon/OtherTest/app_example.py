# app.py
# reference_1:https://www.youtube.com/watch?v=i8ncIcJs-LA&ab_channel=Maso%E7%9A%84%E8%90%AC%E4%BA%8B%E5%B1%8B
# reference_2:https://www.youtube.com/watch?v=uqkJmsb8UIY&ab_channel=Maso%E7%9A%84%E8%90%AC%E4%BA%8B%E5%B1%8B
# reference_3:https://ithelp.ithome.com.tw/users/20142564/articles
# reference_Flask:https://devs.tw/post/448


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
from linebot.models import *

import config
local_port = 3001

app = Flask(__name__)

line_bot_api = LineBotApi(config.channel_access_token)
handler = WebhookHandler(config.channel_secret)

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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run(port=local_port)