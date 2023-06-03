from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials
import os
from PIL import Image


# 取得Custom Vision資源的訂用帳戶金鑰和端點
training_key = '5cd5af885a1f4eb2961b2c696aa2d4a6'
prediction_key = 'ecfbb2ef04c74d11aef28648001e5976'
endpoint = 'https://test202304240853.cognitiveservices.azure.com/'

# 建立訓練和預測的客戶端
credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})
trainer = CustomVisionTrainingClient(endpoint, credentials)

# 取得Custom Vision專案的ID
project_id = 'b8fac83d-ed5b-4ce9-be83-00ed0a1e4445'

tags = trainer.get_tags(project_id)

# 資料夾路徑
folder_path = 'C:/Users/L3510/Desktop/備分/Images/'
folder_name = ['baguette','coconut_tart','donut','egg_tart',
       'garlic_bread','parmesan_cheese_bread','pineapple_bun',
       'red_bean_bun','white_bread','yolk_pastry']

for i in range(0,10):
    folder = folder_path+folder_name[i]
    # 讀取資料夾中的所有檔案
    file_list = os.listdir(folder)
    
    #比對標籤與資料夾名稱
    for tag in tags:
        if(tag.name==folder_name[i]):
            bread_tag = tag.id
    
    # 遍歷每個檔案
    for file_name in file_list:
        # 確認檔案是圖片檔案
        if file_name.endswith('.jpg') or file_name.endswith('.png'):
            # 圖片檔案的完整路徑
            image_path = os.path.join(folder, file_name)
            #加上標籤並上傳至Azure自訂視覺訓練集
            with open(image_path, 'rb') as image_contents:
                image_data = image_contents.read()
                trainer.create_images_from_data(project_id, image_data, [bread_tag])
            #刪除已上傳圖片
            #os.remove(image_path)

print('圖片已成功上傳至Custom Vision專案。')

