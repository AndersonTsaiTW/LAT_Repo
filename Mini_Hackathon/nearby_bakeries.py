import requests
#from geopy.distance import geodesic
#from linebot.models import *

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

'''
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
'''

#lat = str(25.040213)
#lng = str(121.512384)
#print(get_nearby_bakeries(lat, lng))