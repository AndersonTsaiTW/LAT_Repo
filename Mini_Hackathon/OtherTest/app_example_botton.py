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
    if event.message.text == '問題':
        reply_message = TextSendMessage(text='这是答案，您对这个答案满意吗？')
        # 使用 ButtonsTemplate 创建选项菜单
        buttons_template = TemplateSendMessage(
            alt_text='顾客回饋评分',
            template=ButtonsTemplate(
                title='请给出您的评分',
                text='请点击下方按钮进行评分',
                actions=[
                    PostbackAction(
                        label='0分',
                        data='score_0'
                    ),
                    PostbackAction(
                        label='1分',
                        data='score_1'
                    ),
                    PostbackAction(
                        label='2分',
                        data='score_2'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, [reply_message, buttons_template])


# 处理回饋评分的回调函数
@handler.add(PostbackEvent)
def handle_postback(event):
    # 获取回调数据
    data = event.postback.data

    if data.startswith('score_'):
        score = int(data.split('_')[1])
        # 存储回饋评分，可以使用数据库或其他存储方式进行存储操作
        # ...

        # 回复顾客评分结果
        reply_text = f"您给出了{score}分评分，谢谢您的反馈！"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text)
        )



if __name__ == "__main__":
    app.run(port=local_port)