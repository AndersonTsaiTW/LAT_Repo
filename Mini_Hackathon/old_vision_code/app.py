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
from geopy.distance import geodesic
import os
import requests
import string
import old_vision_code.chatgptENG as chatgptENG
import old_vision_code.brtestpr1 as brtestpr1
import local_bread
import re
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


@handler.add(MessageEvent, message=(ImageMessage,TextMessage,LocationMessage))
def handle_message(event):
    if isinstance(event.message, TextMessage):
        bread_names = ["法式長棍麵包", "羊角麵包", "甜甜圈", "蜂蜜羅宋", "羅塞達麵包", "黃金菠蘿包", "布裡麵包",
                       "鄉村麵包", "凱撒森梅爾", "全麥麵包"]
        for bread_name in bread_names:
            if bread_name in event.message.text:
                reply_text = chatgptENG.chatgptfn(bread_name)
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=reply_text.choices[0].message.content))

        if event.message.text == "你好":
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
        if event.message.text == "麵包辨識器!":
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

        elif event.message.text == "傳送圖片":
            content = "請給我一張你想要知道的麵包圖片吧!"
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=content))


        elif event.message.text == "哪裡有好吃的麵包店!!!":
            content = "請傳送位置資訊給我，我幫你找出三家好吃的麵包店!"
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=content))

        elif event.message.text == "傳送網址":
            content = "請給我一個你想要知道的麵包網址吧!"
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=content))
        if re.match('告訴我秘密', event.message.text):
            message = text = event.message.text
            if re.match('告訴我秘密', message):
                location_message = LocationSendMessage(
                    title='日治時期的古蹟',
                    address='總統府',
                    latitude=25.040213810016002,
                    longitude=121.51238385108306
                )
                line_bot_api.reply_message(event.reply_token, location_message)
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(message))

        else:
            content = "請稍等我一下"
            # s.append(TextSendMessage(text=content))

            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=content))
            image_url = event.message.text
            breadtag = brtestpr1.breadpredict(image_url)
            reply_text = chatgptENG.chatgptfn(breadtag)
            # content = "請稍等我一下"
            # # s.append(TextSendMessage(text=content))
            #
            # line_bot_api.reply_message(
            #     event.reply_token,
            #     TextSendMessage(text=content))
            # s.append(TextSendMessage(text=reply_text.choices[0].message.content))
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=reply_text.choices[0].message.content))
                # TextSendMessage(text=reply_text.choices[0].message.content))


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
    if isinstance(event.message, LocationMessage):
        # addr = event.message.address  # 地址
        # lat = str(event.message.latitude)  # 緯度
        # lon = str(event.message.longitude)  # 緯度
        # # line_bot_api.reply_message(yourToken, [reply_txt, reply_stk])
        #
        # if addr is None:
        #     msg = f'收到GPS座標:({lat},{lon})\n謝謝!'
        # else:
        #     msg = f'收到GPS座標:({lat},{lon})\n地址:{addr}!'
        #
        # reply_msg = TextSendMessage(text=msg)
        # line_bot_api.reply_message(event.reply_token, reply_msg)


        ###
        # from geopy.distance import geodesic
        #
        # # 假設有三個店家的位置資訊
        # stores = [
        #     {
        #         'name': 'Boulangerie Ours',
        #         'address': 'Boulangerie Ours',
        #         'latitude': 25.025838552815568,
        #         'longitude': 121.54859409593915,
        #         'image_url': 'https://i.pinimg.com/236x/80/1e/3a/801e3a8cd8075102778e2d4aae42f118.jpg'
        #     },
        #     {
        #         'name': '店家B',
        #         'address': '地址B',
        #         'latitude': 25.040213,
        #         'longitude': 121.512384,
        #         'image_url': 'https://i.pinimg.com/236x/e2/69/48/e26948e111499bcb7d5d69aecff0ae7c.jpg'
        #     },
        #     {
        #         'name': '店家C',
        #         'address': '地址C',
        #         'latitude': 25.036417,
        #         'longitude': 121.517052,
        #         'image_url': 'https://i.pinimg.com/564x/c7/15/e3/c715e350d8293707240677fe4765e921.jpg'
        #     }
        # ]
        # addr = event.message.address
        # # 使用者提供的經緯度
        # user_latitude = str(event.message.latitude)
        # user_longitude = str(event.message.longitude)
        #
        # # 計算使用者與每個店家的距離
        # distances = []
        # for store in stores:
        #     store_latitude = store['latitude']
        #     store_longitude = store['longitude']
        #     distance = geodesic((user_latitude, user_longitude), (store_latitude, store_longitude)).kilometers
        #     distances.append((store['name'], store['address'], distance, store['image_url']))
        #
        # # 根據距離排序，取得前三名店家
        # closest_stores = sorted(distances, key=lambda x: x[2])[:3]
        #
        # # 製作 carousel 的 columns
        # carousel_columns = []
        # for store in closest_stores:
        #     store_name = store[0]
        #     store_address = store[1]
        #     store_distance = store[2]
        #     store_image_url = store[3]
        #     column = CarouselColumn(
        #         thumbnail_image_url=store_image_url,
        #         title=store_name,
        #         text=f'地址：{store_address}\n距離：{store_distance:.2f} 公里',
        #         actions=[
        #             MessageAction(label='查看詳情', text=f'詳情 {store_name}')
        #         ]
        #     )
        #     carousel_columns.append(column)
        #
        # # 建立 Carousel Template
        # carousel_template = CarouselTemplate(columns=carousel_columns)
        #
        # # 建立 TemplateSendMessage
        # reply_msg = TemplateSendMessage(alt_text='最接近的三個店家', template=carousel_template)
        #
        # line_bot_api.reply_message(event.reply_token, reply_msg)

        ###
        def get_nearby_bakeries(lat, lng):
            GOOGLE_API_KEY = 'AIzaSyCnXqX2MVkzGHxiUtmez4MHtAxDk8qN5u0'

            # 使用 Google Places API 搜尋附近的麵包店
            foodStoreSearch = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?key={}&location={},{}&rankby=distance&type=bakery&language=zh-TW'.format(
                GOOGLE_API_KEY, lat, lng)
            foodReq = requests.get(foodStoreSearch)
            nearby_restaurants_dict = foodReq.json()
            top20_restaurants = nearby_restaurants_dict["results"]

            # 計算距離並排序
            restaurant_distances = []
            for restaurant in top20_restaurants:
                destination_lat = restaurant["geometry"]["location"]["lat"]
                destination_lng = restaurant["geometry"]["location"]["lng"]
                distance_url = 'https://maps.googleapis.com/maps/api/distancematrix/json?key={}&origins={},{}&destinations={},{}&language=zh-TW'.format(
                    GOOGLE_API_KEY, lat, lng, destination_lat, destination_lng)
                distance_req = requests.get(distance_url)
                distance_data = distance_req.json()
                distance = distance_data["rows"][0]["elements"][0]["distance"]["text"]
                rating = restaurant.get("rating", 0)
                if rating > 4.5:
                    restaurant_distances.append((restaurant, distance))

            # 根據距離排序取得前三個餐廳
            sorted_restaurants = sorted(restaurant_distances, key=lambda x: x[1])[:3]

            return sorted_restaurants

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
        restaurants = get_nearby_bakeries(lat, lng)

        # 建立 Carousel Template
        # 建立 Carousel Template
        GOOGLE_API_KEY = 'AIzaSyCnXqX2MVkzGHxiUtmez4MHtAxDk8qN5u0'
        carousel_template = create_carousel_template(restaurants, GOOGLE_API_KEY)

        # 建立 TemplateSendMessage
        carousel_message = TemplateSendMessage(alt_text="附近麵包店", template=carousel_template)

        # 回覆訊息給使用者
        line_bot_api.reply_message(event.reply_token, carousel_message)


if __name__ == "__main__":
    app.run(port=local_port)