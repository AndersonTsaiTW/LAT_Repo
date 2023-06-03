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

# 创建 ConfirmTemplate
confirm_template = TemplateSendMessage(
    alt_text='确认模板',
    template=ConfirmTemplate(
        text='您确定要删除此条消息吗？',
        actions=[
            MessageAction(
                label='确定',
                text='是的'
            ),
            MessageAction(
                label='取消',
                text='不'
            )
        ]
    )
)

# 处理确认模板的回调函数
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_input = event.message.text

    if user_input == '是的':
        # 执行删除操作
        # ...

        # 回复确认结果
        reply_text = '消息已删除。'
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text)
        )
    elif user_input == '不':
        # 取消操作
        # ...

        # 回复取消结果
        reply_text = '操作已取消。'
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text)
        )
    else:
        # 其他回复
        # ...

        # 发送确认模板
        line_bot_api.reply_message(
            event.reply_token,
            confirm_template
        )


if __name__ == "__main__":
    app.run(port=local_port)