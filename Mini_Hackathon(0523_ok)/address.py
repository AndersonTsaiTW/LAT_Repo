import requests
import urllib.request
import json
import time
import random
GOOGLE_API_KEY = 'AIzaSyCODxfHdAAkuJp-FJl1mHkzrL30EUbCsAg'


def get_latitude_longtitude():
    # decode url
    address = '100台北市中正區汀州路三段184號'
    url = 'https://maps.googleapis.com/maps/api/geocode/json?key={}&address={}&sensor=false'.format(GOOGLE_API_KEY,address)

    while True:
        res = requests.get(url)
        js = json.loads(res.text)

        if js["status"] != "OVER_QUERY_LIMIT":
            time.sleep(1)
            break

    result = js["results"][0]["geometry"]["location"]
    lat = result["lat"]
    lng = result["lng"]
    print(lat, lng)
    return lat, lng
# get_latitude_longtitude()
# ========
# address = '100台北市中正區汀州路三段184號'
# lat='25.0129193'
# lng='121.5348485'
# # GOOGLE_API_KEY = 'AIzaSyCODxfHdAAkuJp-FJl1mHkzrL30EUbCsAg'
# # foodStoreSearch= 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?key={}&location={},{}&rankby=distance&type=restaurant&language=zh-TW'.format(GOOGLE_API_KEY, lat, lng)
# foodStoreSearch='https://maps.googleapis.com/maps/api/place/nearbysearch/json?key=AIzaSyCnXqX2MVkzGHxiUtmez4MHtAxDk8qN5u0&location=25.0129193,121.5348485&rankby=distance&type=restaurant&language=zh-TW'
# foodReq=requests.get(foodStoreSearch)
# nearby_restaurants_dict=foodReq.json()
# top20_restaurants=nearby_restaurants_dict["results"]
# res_num= (len(top20_restaurants))
# # foodReq.json()
# bravo=[]
# # print(foodReq.json())
# for i in range(res_num):
#     try:
#         if top20_restaurants[i]['rating'] > 3.9:
#             print('rate: ', top20_restaurants[i]['rating'])
#             bravo.append(1)
#     except:
#         KeyError
#     if len(bravo) == 0:
#         content="沒東西可以吃"
#
# #restaurant random.choice(top2e_restaurants) YEAR —
#
# # restaurant=top20_restaurants[random.choice(bravo)]
# if len(bravo) > 0:
#     restaurant = top20_restaurants[random.choice(bravo)]
#     # .根據,最多只有一張照片
#     photo_reference = restaurant["photos"][0]["photo_reference"]
#     photo_width = restaurant["photos"][0]["width"]
#     thumbnail_image_url = "https://maps.googleapis.com/maps/api/place/photo?key={}&photoreference={}&maxwidth={}".format(
#         GOOGLE_API_KEY, photo_reference,photo_width)
#
#     rating = "無" if restaurant.get("rating") is None else restaurant["rating"]
#     address = "沒有資料" if restaurant.get("vicinity") is None else restaurant["vicinity"]
#     details = "Google Map評分:{}\n地址:{}".format(rating, address)
#     print(details)
#     # 其他程式碼
# else:
#     restaurant = None  # 或者根據需求進行處理
#
# if restaurant.get("photos") is None:
#     thumbnail_image_url = None
# else:
#     # .根據,最多只有一張照片
#     photo_reference = restaurant["photos"][0]["photo_reference"]
#     photo_width = restaurant["photos"][0]["width"]
#     thumbnail_image_url="https://maps.googleapis.com/maps/api/place/photo?key={}&photoreference={}&maxwidth={}".format(GOOGLE_API_KEY, photo_reference,photo_width)
#
# rating="無" if restaurant.get("rating") is None else restaurant["rating"]
# address = "沒有資料" if restaurant.get("vicinity") is None else restaurant ["vicinity"]
# details="Google Map評分:{}\n地址:{}".format(rating, address)
#
# print(details)
# map_url="https://www.google.com/maps/search/?api=1&query={lat}{long}&query_place_id={place_id}".format(lat=restaurant["geometry"]["location"]["lat"],long=restaurant ["geometry"]["location"]["lng"],place_id=restaurant["place_id"])
# print(map_url)
# =====================
import requests

address = '100台北市中正區汀州路三段184號'
lat = '25.0129193'
lng = '121.5348485'
GOOGLE_API_KEY = 'AIzaSyCnXqX2MVkzGHxiUtmez4MHtAxDk8qN5u0'

# 取得餐廳列表
foodStoreSearch = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?key={}&location={},{}&rankby=distance&type=bakery&language=zh-TW'.format(GOOGLE_API_KEY, lat, lng)
foodReq = requests.get(foodStoreSearch)
nearby_restaurants_dict = foodReq.json()
top20_restaurants = nearby_restaurants_dict["results"]

# 計算距離並排序
restaurant_distances = []
for restaurant in top20_restaurants:
    destination_lat = restaurant["geometry"]["location"]["lat"]
    destination_lng = restaurant["geometry"]["location"]["lng"]
    distance_url = 'https://maps.googleapis.com/maps/api/distancematrix/json?key={}&origins={},{}&destinations={},{}&language=zh-TW'.format(GOOGLE_API_KEY, lat, lng, destination_lat, destination_lng)
    distance_req = requests.get(distance_url)
    distance_data = distance_req.json()
    distance = distance_data["rows"][0]["elements"][0]["distance"]["text"]
    rating = restaurant.get("rating", 0)
    if rating > 4.5:
        restaurant_distances.append((restaurant, distance))

# 根據距離排序取得前三個餐廳
sorted_restaurants = sorted(restaurant_distances, key=lambda x: x[1])[:3]

# 輸出前三個餐廳的所有資訊
for restaurant, distance in sorted_restaurants:
    name = restaurant["name"]
    address = restaurant["vicinity"]
    rating = restaurant.get("rating", "無評分")
    photos = restaurant.get("photos", [])
    if photos:
        photo_reference = photos[0].get("photo_reference")
        photo_width = photos[0].get("width")
        thumbnail_image_url = f"https://maps.googleapis.com/maps/api/place/photo?key={GOOGLE_API_KEY}&photoreference={photo_reference}&maxwidth={photo_width}"
    else:
        thumbnail_image_url = None

    print("餐廳名稱:", name)
    print("地址:", address)
    print("評分:", rating)
    print("距離:", distance)
    print("照片連結:", thumbnail_image_url)
    print("==========")