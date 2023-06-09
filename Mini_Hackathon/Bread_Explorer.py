from flask import Flask, request, abort

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,ImageMessage
)
from geopy.distance import geodesic
import os
import requests
import datetime
import random

#自行寫作的功能部件
#import old_vision_code.chatgptENG as chatgptENG
import chatgptENG_cal
#import brtestpr1
import url_bread
import local_bread
import nearby_bakeries
#import re

#儲存共同變量與token的檔案
import config
local_port = 3001

app = Flask(__name__)

line_bot_api = LineBotApi(config.channel_access_token)
handler = WebhookHandler(config.channel_secret)
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
#紀錄待寫入的全域變數與開關區
#麵包種類
breadtag_rec = ""
#chatGPT回應
reply_rec = ""
#是否要紀錄(如果麵包分類錯誤就不紀錄訊息)
rec = False
#是否為照片
pic = False
#照片位置
path_rec = ""
#要不要儲存這張照片(分類錯誤要儲存，之後update模型用)
pic_copy = False
#是不是fakeGPT的假訊息，是的話要進直接紀錄評價流程
fake = False
#如果是fakeGPT訊息，那是第幾號訊息，index為何
index_rec = ""

@handler.add(MessageEvent, message=(ImageMessage,TextMessage,LocationMessage))
def handle_message(event):
    #宣告全域變數，並監控全域變數狀態
    global breadtag_rec, reply_rec, rec, pic, path_rec, pic_copy, fake, index_rec
    print("breadtag_rec:",breadtag_rec, "reply_rec:", reply_rec[0:10],
    "rec:", rec, "pic:", pic,"path_rec:", path_rec, "pic_copy:", pic_copy,
    "fake:", fake, "index_rec:", index_rec) 
    #判斷網址的狀況，並把網址送入azure分析後，到chatGPT產結果回傳
    if isinstance(event.message, TextMessage):
        if event.message.text.startswith("https:"):
            image_url = event.message.text
            breadtag = url_bread.breadpredict(image_url)
            if breadtag == 'error':
                line_bot_api.reply_message(event.reply_token,
                TextSendMessage(text="這不是圖片的網址喔！"))
            elif breadtag == 'no_bread':
                line_bot_api.reply_message(event.reply_token,
                TextSendMessage(text="這圖片裡好像找不到麵包？"))
            else:
                #用fakeGPT取出這種麵包有幾筆記錄，目前的回覆評價加總是多少
                fakegpt = chatgptENG_cal.fakegptfn(breadtag)
                #計算仍要使用chatGPT的機率，至少保持20%以便讓新的回應能夠生成
                #把chatGPT回應的價值度預設為5，再去計算這個回應佔現有價值度多少
                #如果現在一個有效回應都沒有，或是儲存的回應都是0分，會100%取chatGPT產回應
                #隨著有效回應越來越多，會持續減少使用chatGPT的數量到20%
                real_p = max(0.2, 5 / (fakegpt[0]+5))
                rate = random.random()
                if rate > real_p:
                    reply_text = fakegpt[2]

                    index_rec = fakegpt[1]
                    fake = True
                else:
                    reply_text = chatgptENG_cal.chatgptfn(breadtag)

                breadtag_rec = breadtag
                reply_rec = reply_text
                rec = True

                #print("correct")
                #回覆意見選單
                satisfaction_message = TemplateSendMessage(
                    alt_text='滿意程度評價',
                    template=ButtonsTemplate(
                        text='請問您對這個答案滿意嗎？',
                        actions=[
                            MessageTemplateAction(label='滿意：2分', text=2),
                            MessageTemplateAction(label='勉強滿意：1分', text=1),
                            MessageTemplateAction(label='沒用的答案:0分', text=0),
                            MessageTemplateAction(label='根本不是這個麵包吧:扣分', text=-1)
                        ]
                    )
                )
                # 回覆答案消息和滿意度評價選單消息
                line_bot_api.reply_message(event.reply_token, 
                [TextSendMessage(text=reply_text), satisfaction_message])
                #print(breadtag_rec)
                #print(reply_rec[0:10])
                #print(rec)
                #return breadtag_rec, reply_rec, rec

        ###以下是依使用者回覆進行儲存的程式碼區###
        #如果是fakeGPT的假訊息，紀錄回覆評價，無論他是什麼值
        #因為他條件最多，所以要放最前面
        elif event.message.text in ["2","1","0","-1"] and rec and fake:
            try:
                chatgptENG_cal.breadfakerecord(breadtag_rec, index_rec, int(event.message.text))

                breadtag_rec = reply_rec = path_rec = index_rec = ""
                rec = pic = pic_copy = fake = False
                #breadtag_rec = ""
                #reply_rec = ""
                #rec = False
                #pic = False
                #fake = False
                #index_rec = ""

            except(KeyError, IndexError):
                breadtag_rec = reply_rec = path_rec = index_rec = ""
                rec = pic = pic_copy = fake = False


            line_bot_api.reply_message(event.reply_token, 
            TextSendMessage(text="謝謝你，我們會再努力"))
            #breadtag_rec, reply_rec, path_rec, index_rec = ""
            #rec, pic, pic_copy, fake = False

        #chatGPT的回應，用戶如果還算滿意就記錄起來
        elif event.message.text in ["2","1","0"] and rec:
            line_bot_api.reply_message(event.reply_token, 
            TextSendMessage(text="謝謝你，我們會再努力"))
            chatgptENG_cal.breadchatrecord(breadtag_rec, reply_rec, int(event.message.text))
            breadtag_rec = reply_rec = path_rec = index_rec = ""
            rec = pic = pic_copy = fake = False
            #breadtag_rec = ""
            #reply_rec = ""
            #rec = False
            #pic = False

        #類別不對而且是照片的時候，照片存起來以後訓練模型用
        elif event.message.text =='-1' and rec and pic:
            #原本想使用麵包清單自動建立lineBOT選單，尚未完成
            '''
            options = list(config.breaddict.keys())

            # 建立CarouselTemplate的清單值
            columns = []
            for option in options:
                column = CarouselColumn(
                    text=config.breaddict[option],
                    actions=[
                        MessageTemplateAction(label=config.breaddict[option], text=option)
                    ]
                )
                columns.append(column)
            #補上以上皆非的選項
            column = CarouselColumn(
                text="這些都不是",
                actions=[MessageTemplateAction(label="這些都不是", text="這些都不是")])
            columns.append(column)
            print(columns)

            #建立CarouselTemplate
            carousel_template = CarouselTemplate(columns=columns)

            satisfaction_message = TemplateSendMessage(
                alt_text='這是哪一種麵包？',
                template=carousel_template
            )
            '''
            #想紀錄、是照片、而且使用者說類別錯誤=打開照片紀錄開關
            pic_copy = True

            content = "真抱歉，我們會再努力，那這張照片是以下這些麵包的其中一種嗎？\n請幫我輸入他們的英文名稱告訴我喔，謝謝你的幫忙～\n"

            breadlist_msg = ""
            a = 1
            for i in config.breaddict:
                breadlist_msg = breadlist_msg + "\n" + str(a) + ". " + config.breaddict[i] +"：請輸入  " + i
                a = a + 1
            
            content_last = "\n\n如果都不是這些麵包，請幫我輸入  all_wrong"

            line_bot_api.reply_message(event.reply_token, 
            TextSendMessage(text=content+breadlist_msg+content_last))
        #訊息是麵包名稱，而且痊癒變數判斷是要紀錄的照片時，把照片另外依類別存檔
        elif (event.message.text in config.breaddict or event.message.text == "all_wrong") and rec and pic and pic_copy:
            #存到各自分類資料夾，以時間作為檔名
            target_folder = "./update/{}/".format(event.message.text)
            current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            target_filename = current_time + ".jpg"
            target_path = target_folder + target_filename
            
            with open(path_rec, 'rb') as source_file:
                with open(target_path, 'wb') as target_file:
                    target_file.write(source_file.read())
            
            line_bot_api.reply_message(event.reply_token, 
            TextSendMessage(text="謝謝你，我們會繼續變厲害的～"))
            #reset全域變數
            breadtag_rec = reply_rec = path_rec = index_rec = ""
            rec = pic = pic_copy = fake = False
            #breadtag_rec = ""
            #reply_rec = ""
            #rec = False
            #pic = False
            #path_rec = ""
            #pic_copy = False

        #非照片訊息，用戶不滿意就說抱歉，不記錄，並且清空全域變量
        elif event.message.text == '-1' and rec:
            line_bot_api.reply_message(event.reply_token, 
            TextSendMessage(text="真抱歉，我們會再努力"))
            #reset全域變數
            breadtag_rec = reply_rec = path_rec = index_rec = ""
            rec = pic = pic_copy = fake = False
            #breadtag_rec = ""
            #reply_rec = ""
            #rec = False
            #pic = False
        

        ###以上是儲存程式碼區###

        elif event.message.text == "你好":
            buttons_template = TemplateSendMessage(
                alt_text='啟動服務',
                template=ButtonsTemplate(
                    title='你想選擇哪種圖像辨識的服務呢?',
                    text='請選擇',
                    thumbnail_image_url='https://i.imgur.com/gt4Ke6o.jpg',
                    actions=[
                        MessageTemplateAction(
                            label='麵包辨識器!',
                            text='麵包辨識器!'
                        ),
                        MessageTemplateAction(
                            label='你絕對不會都知道的10種麵包!',
                            text='你絕對不會都知道的10種麵包!'
                        ),
                        MessageTemplateAction(
                            label='哪裡有好吃的麵包店!!!',
                            text='哪裡有好吃的麵包店!!!'
                        )
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token, buttons_template)

        elif event.message.text == "麵包辨識器!":
            buttons_template = TemplateSendMessage(
                alt_text='請選擇',
                template=ButtonsTemplate(
                    title='你想傳什麼樣的照片呢?',
                    text='請選擇',
                    thumbnail_image_url='https://i.pinimg.com/236x/8e/81/96/8e81968b3ba91641fa4aecacfd1c85bf.jpg',
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

        elif event.message.text == "你絕對不會都知道的10種麵包!":
            Image_Carousel = TemplateSendMessage(
                alt_text='麵包種類展示',
                template=ImageCarouselTemplate(
                    columns=[
                        ImageCarouselColumn(
                            image_url='https://i.pinimg.com/564x/98/af/1a/98af1aa91d35ea127554dafa4e013c4a.jpg',
                            action=PostbackTemplateAction(
                                label='法式長棍麵包',
                                text='我想了解法式長棍麵包',
                                data='action=buy&itemid=1'
                            )
                        ),
                        ImageCarouselColumn(
                            image_url='https://i.pinimg.com/564x/58/ba/79/58ba79caee073b566f1632f8fe813c03.jpg',
                            action=PostbackTemplateAction(
                                label='羊角麵包',
                                text='我想了解羊角麵包',
                                data='action=buy&itemid=2'
                            )
                        ),
                        ImageCarouselColumn(
                            image_url='https://i.pinimg.com/564x/6b/48/ed/6b48edc930aba93c6df9364dcc20406c.jpg',
                            action=PostbackTemplateAction(
                                label='甜甜圈',
                                text='我想了解甜甜圈',
                                data='action=buy&itemid=2'
                            )
                        ),
                        ImageCarouselColumn(
                            image_url='https://i.pinimg.com/564x/bc/10/16/bc1016e4bde4a07258aca188df6fa114.jpg',
                            action=PostbackTemplateAction(
                                label='蜂蜜羅宋',
                                text='我想了解蜂蜜羅宋',
                                data='action=buy&itemid=2'
                            )
                        ),
                        ImageCarouselColumn(
                            image_url='https://i1.kknews.cc/cZqsLxI43ZPK_74mxrax6cUKFNnoUEK8Tw/0.jpg',
                            action=PostbackTemplateAction(
                                label='羅塞達麵包',
                                text='我想了解羅塞達麵包',
                                data='action=buy&itemid=2'
                            )
                        ),
                        ImageCarouselColumn(
                            image_url='https://i.pinimg.com/564x/ea/2a/0b/ea2a0b20ed098f2f56285d469fe82a0b.jpg',
                            action=PostbackTemplateAction(
                                label='黃金菠蘿包',
                                text='我想了解黃金菠蘿包',
                                data='action=buy&itemid=2'
                            )
                        ),
                        ImageCarouselColumn(
                            image_url='https://i2.kknews.cc/qImj8jZ4xpZcmDy_P8MrS0IskTJsW5kd9w/0.jpg',
                            action=PostbackTemplateAction(
                                label='布裡麵包',
                                text='我想了解布裡麵包',
                                data='action=buy&itemid=2'
                            )
                        ),
                        ImageCarouselColumn(
                            image_url='https://i1.kknews.cc/INvsLWqaDezRG2tVROy_LOxkAV-m4Jyd_Q/0.jpg',
                            action=PostbackTemplateAction(
                                label='鄉村麵包',
                                text='我想了解鄉村麵包',
                                data='action=buy&itemid=2'
                            )
                        ),
                        ImageCarouselColumn(
                            image_url='https://i2.kknews.cc/oo99eLRnGNPKsO2DNLn4Pw80eji735v-Zw/0.jpg',
                            action=PostbackTemplateAction(
                                label='凱撒森梅爾',
                                text='我想了解凱撒森梅爾',
                                data='action=buy&itemid=2'
                            )
                        ),
                        ImageCarouselColumn(
                            image_url='https://i1.kknews.cc/j99GWhgnZ6aPUisZnO9YiYsrI-gNnsenYQ/0.jpg',
                            action=PostbackTemplateAction(
                                label='全麥麵包',
                                text='我想了解全麥麵包',
                                data='action=buy&itemid=2'
                            )
                        )
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token, Image_Carousel)
        
        #當句子開頭為"我想了解"，且內容包含10個icon的麵包時，直接傳送chatGPT給出說明
        elif event.message.text.startswith("我想了解"):
            #breadicon的列表，之後應該往前提，讓icon選單也變成自動生成，減少維運成本
            bread_icons = ["法式長棍麵包", "羊角麵包", "甜甜圈", "蜂蜜羅宋", "羅塞達麵包", "黃金菠蘿包", "布裡麵包","鄉村麵包", "凱撒森梅爾", "全麥麵包"]
            for bread_name in bread_icons:
                #print(bread_name)
                #print(bread_name in event.message.text)
                if bread_name in event.message.text:
                    reply_text = chatgptENG_cal.chatgptfn(bread_name)
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=reply_text))         
        
        elif event.message.text == "哪裡有好吃的麵包店!!!":
            content = "請傳送位置資訊給我，我幫你找出三家好吃的麵包店!"
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=content))

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
            content = ["請對我說「你好」，就可以叫出選單","或是你也可以直接提供麵包圖片網址或照片，我們會教你它的英文與知識"]
            line_bot_api.reply_message(event.reply_token,[TextSendMessage(text=msg) for msg in content])
            
    elif isinstance(event.message, ImageMessage):
        #ext = 'jpg'
        image_content = line_bot_api.get_message_content(event.message.id)
        #自動把使用者傳出的照片編號並且存到資料夾中
        directory = './static/'
        existing_images = len(os.listdir(directory))
        next_image_number = existing_images + 1
        print(next_image_number)
        image_number_str = str(next_image_number).zfill(4)
        image_name = image_number_str + '.jpg'
        #記錄這張照片的位置，寫成path
        path = directory + image_name
        #把照片存到指定的資料夾裡面
        with open(path, 'wb') as fd:
            for chunk in image_content.iter_content():
                fd.write(chunk)

        image_url = os.path.join(directory, image_name)
        breadtag = local_bread.breadpredict(image_url)
        if breadtag == 'no_bread':
            line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text="這圖片裡好像找不到麵包？"))
        else:
            #用fakeGPT取出這種麵包有幾筆記錄，目前的回覆評價加總是多少
            fakegpt = chatgptENG_cal.fakegptfn(breadtag)
            #計算仍要使用chatGPT的機率，至少保持20%以便讓新的回應能夠生成
            #把chatGPT回應的價值度預設為5，再去計算這個回應佔限有價值度多少
            #如果現在一個有效回應都沒有，或是儲存的回應都是0分，會100%取chatGPT產回應
            #隨著有效回應越來越多，會持續減少使用chatGPT的數量到20%
            real_p = max(0.2, 5 / (fakegpt[0]+5))
            rate = random.random()
            if rate > real_p:
                reply_text = fakegpt[2]
                #fakeGPT全域變數啟動
                index_rec = fakegpt[1]
                fake = True
            else:
                reply_text = chatgptENG_cal.chatgptfn(breadtag)
                path_rec = path
            #全域變數：麵包tag紀錄、回覆訊息記錄、紀錄開關open
            #全域變數：圖片開關open、圖像檔path紀錄
            breadtag_rec = breadtag
            reply_rec = reply_text
            rec = True
            pic = True

            #回饋選單
            satisfaction_message = TemplateSendMessage(
                alt_text='滿意程度評價',
                template=ButtonsTemplate(
                    text='請問您對這個答案滿意嗎？',
                    actions=[
                        MessageTemplateAction(label='滿意：2分', text=2),
                        MessageTemplateAction(label='勉強滿意：1分', text=1),
                        MessageTemplateAction(label='沒用的答案:0分', text=0),
                        MessageTemplateAction(label='根本不是這個麵包吧:扣分', text=-1)
                    ]
                )
            )
            # 回覆答案消息和滿意度評價選單消息
            line_bot_api.reply_message(event.reply_token, 
            [TextSendMessage(text=reply_text), satisfaction_message])

    elif isinstance(event.message, LocationMessage):
        #已經另外寫作nearby_bakeries.py，輸入經緯度即可得到最近的三家麵包店列表
        #先定義create_carousel_template函數確立表達方式以備後續使用
        def create_carousel_template(restaurants, api_key):
            carousel_columns = []
            for restaurant, distance in restaurants:
                name = restaurant["name"]
                # 將標題縮短至小於40字元
                name = name[:37] + "..." if len(name) > 40 else name
                address = restaurant["vicinity"]
                rating = restaurant.get("rating", "無評分")
                photos = restaurant.get("photos", [])
                if photos:
                    photo_reference = photos[0].get("photo_reference")
                    photo_width = photos[0].get("width")
                    thumbnail_image_url = f"https://maps.googleapis.com/maps/api/place/photo?key={api_key}&photoreference={photo_reference}&maxwidth={photo_width}"
                else:
                    thumbnail_image_url = None

                destination_lat = restaurant["geometry"]["location"]["lat"]
                destination_lng = restaurant["geometry"]["location"]["lng"]
                actions = [
                    URIAction(label="查看地圖",
                              uri=f"https://www.google.com/maps/search/?api=1&query={destination_lat},{destination_lng}")
                ]

                # 建立 Carousel Column
                column = CarouselColumn(
                    thumbnail_image_url=thumbnail_image_url,
                    title=name,
                    text=f"地址: {address}\n評分: {rating}\n距離: {distance}",
                    actions=actions
                )
                carousel_columns.append(column)

            carousel_template = CarouselTemplate(columns=carousel_columns)
            return carousel_template

        # 取得使用者傳送的經緯度位置
        lat = str(event.message.latitude)
        lng = str(event.message.longitude)
        # 取得前三家附近的麵包店資訊
        restaurants = nearby_bakeries.get_nearby_bakeries(lat, lng)
        # 建立 Carousel Template
        carousel_template = create_carousel_template(restaurants, config.google_api_key)
        # 建立 TemplateSendMessage
        carousel_message = TemplateSendMessage(alt_text="附近麵包店", template=carousel_template)

        # 回覆訊息給使用者
        line_bot_api.reply_message(event.reply_token, carousel_message)

if __name__ == "__main__":
    app.run(port=local_port)