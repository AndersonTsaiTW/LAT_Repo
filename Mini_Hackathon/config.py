channel_access_token = "23uRE8qB1LbXm8pngifTyRsCVqzW6voA1XPT7hPkHkPbjVqwv6mEB0yERdS272A0gTVLO+78v/13izdnyxkmETscJbqy8HwcfuLD4DJQkHn9xzKH69eSNmelW2ssiOm21Ez+L+5SdZd/O4xRcycNnQdB04t89/1O/w1cDnyilFU="
channel_secret = "d1793208aa7e0d0716a1a4d90a04dbff"

azure_model_endpoint = "https://test202304240802.cognitiveservices.azure.com/"
azure_model_key = "b9e345f19fc64b31a67332059b32ce56"

azure_brmodel_img_store = "https://test202304240853-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/b8fac83d-ed5b-4ce9-be83-00ed0a1e4445/classify/iterations/bread0527/image"
azure_brmodel_key = "ecfbb2ef04c74d11aef28648001e5976"

google_api_key = 'AIzaSyCnXqX2MVkzGHxiUtmez4MHtAxDk8qN5u0'

breadlist = [
    "baguette",
    "coconut_tart",
    "donut",
    "egg_tart",
    "garlic_bread",
    "parmesan_cheese_bread",
    "pineapple_bun",
    "red_bean_bun",
    "white_bread",
    "yolk_pastry"
    ]
breaddict = {
    "baguette":"法式長棍麵包",
    "coconut_tart":"椰撻",
    "donut":"甜甜圈",
    "egg_tart":"蛋撻",
    "garlic_bread":"大蒜麵包",
    "parmesan_cheese_bread":"巴馬干酪麵包",
    "pineapple_bun":"菠蘿麵包",
    "red_bean_bun":"紅豆麵包",
    "white_bread":"白土司",
    "yolk_pastry":"蛋黃酥"
    }


#a = "巴馬干酪麵包"
#for key, value in breaddict.items():
#    if value == a:
#        print(key)

bread_icons = ["法式長棍麵包", "羊角麵包", "甜甜圈", "蜂蜜羅宋", "羅塞達麵包",
"黃金菠蘿包", "布裡麵包","鄉村麵包", "凱撒森梅爾", "全麥麵包"]

bread_all = breadlist+bread_icons

#print(str(breaddict))