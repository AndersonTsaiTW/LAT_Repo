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

# 定义列表包含每个 ConfirmTemplate 的内容
confirm_content = [
    {
        'text': '确认选项1',
        'action': '动作1'
    },
    {
        'text': '确认选项2',
        'action': '动作2'
    }
]

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == '問題':
        #reply_message = TextSendMessage(text='这是答案，您对这个答案满意吗？')
        # 使用 ButtonsTemplate 创建选项菜单
# 生成 MessageAction 列表
        actions = []
        for content in confirm_content:
            action = MessageAction(
                label=content['text'],
                text=content['action']
            )
            actions.append(action)

        # 创建 ConfirmTemplate
        confirm_template = ConfirmTemplate(
            text='请选择一个选项',
            actions=actions
        )

        # 创建 TemplateSendMessage 并发送
        template_message = TemplateSendMessage(
            alt_text='Confirm Template',
            template=confirm_template
        )

        # 使用 line_bot_api 发送消息
        line_bot_api.reply_message(event.reply_token, template_message)

if __name__ == "__main__":
    app.run(port=local_port)