# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 02:22:27 2023

@author: Leo
"""
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time

import requests
import re
#寫入設定檔
import config

def is_image_url(url):
    # 使用regular expression判斷網址格式
    pattern = r'(http|https)://[^\s]+(.jpg|.jpeg|.png|.gif)'
    match = re.match(pattern, url)
    return bool(match)

def img_identify(img_url):
    subscription_key = config.azure_model_key
    endpoint = config.azure_model_endpoint

    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
    
    tags_result_remote = computervision_client.tag_image(img_url )
    
    detect_list = ['bread','dessert']
    bread_img = 'no'
    
    for tag in tags_result_remote.tags:
        for i in range(0,2):
            if('{}'.format(tag.name) == detect_list[i]):
                bread_img = 'yes'
            #print("'{}' with confidence {:.2f}%".format(tag.name, tag.confidence * 100))
    return bread_img
    

def bread_identify(img_url):
    # 設定請求的標頭和主體
    headers = {
        'Prediction-Key': config.azure_brmodel_key,  # 將 'abc' 替換為您的 Prediction-Key
        'Content-Type': 'application/octet-stream'
    }
    
    # 讀取圖像檔案內容
    #with open(img_url, 'rb') as image_file:  # 將 '<image file>' 替換為您的圖像檔案路徑
    #image_data = image_file.read()

    response1 = requests.get(img_url)
    
    # 檢查圖片下載是否成功
    if response1.status_code == 200:
        image_data = response1.content
        
        # 發送預測請求
        response2 = requests.post(config.azure_brmodel_img_store, headers=headers, data=image_data)  # 將 '<prediction endpoint URL>' 替換為預測端點的 URL
        
        # 處理回應
        if response2.status_code == 200:
            results = response2.json()
            tag = results['predictions'][0]['tagName']
            feedback = tag
        else:
            print('預測請求失敗', response2.status_code, response2.text)
            feedback = 'predict error'
        return feedback
    else:
        feedback = 'download error'
        return feedback

"""主程式"""
def breadpredict(img_url):
    #先判斷是不是圖片網址，不是的話直接回傳error
    #print(is_image_url(img_url))
    if is_image_url(img_url) == False:
        bread = 'error'
    #是圖片網址，才交給模型判斷
    else:
        img_det = img_identify(img_url)
        #print(img_det)
        if(img_det == 'yes'):
            bread = bread_identify(img_url)
            #print(bread)
        else:
            bread = 'no_bread'
    return bread

#images_folder = os.path.join (os.path.dirname(os.path.abspath(__file__)), "images")
#image_url = "https://i.postimg.cc/xjkRY5jt/2.jpg"  #菠蘿麵包照片
#image_url = "https://i.postimg.cc/xjkRY5jt"  #不是照片
#image_url = "https://news.agentm.tw/wp-content/uploads/1-%E6%8B%B7%E8%B2%9D-1.jpg"  #火箭浣熊照片
#abc = breadpredict(image_url)
#print(abc)