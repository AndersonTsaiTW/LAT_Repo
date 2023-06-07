## 麵包探險家(Bread Explorer)
###### 期末專題(end-of-semester project) 
* 專案說明投影片 / Project Description ppt [(連結 / Link)](https://drive.google.com/drive/folders/1O0YNpWWHMssmgJTJc4bRilS4C7HKuTLE)
* 專案成員 / Members: [數學113 蔡尚峰 / Shawn](https://github.com/Shawn0604)、[機電113 鍾孟霖](https://github.com/mlchung1231)、[選讀 蔡昱宏 / Anderson](https://github.com/AndersonTsaiTW)
* 指導老師 / project advisor: 蔡芸琤 / Pecu、鍾祥仁 / Ryan
* 專案特色 / Project Features:  
專案特點：
  1. 協助華語學生學習日常生活中與麵包相關的英語。 / Assist Chinese-speaking students to learn English related to bread in daily life.
  2. 結合 LineBOT、AZURE、chatGPT 等軟件，打造隨時隨地為您提供幫助的 Line 好友。 / Combine LineBOT, AZURE, chatGPT and other software to create Line friends who can assist you wherever you go.
  3. 引入用戶反饋機制，讓服務持續自我優化。 / Introduce a user feedback mechanism so that the service can continue to self-optimize.
* [主程式資料夾 / Folder - Mini_Hackathon](https://github.com/AndersonTsaiTW/LAT_Repo/tree/main/Mini_Hackathon): You can find all the codes here (written in python), including the [主程式碼 / main code](https://github.com/AndersonTsaiTW/LAT_Repo/blob/main/Mini_Hackathon/Bread_Explorer.py), AZURE電腦視覺模型 / AZURE related codes: [url_bread](https://github.com/AndersonTsaiTW/LAT_Repo/blob/main/Mini_Hackathon/url_bread.py) and [local_bread](https://github.com/AndersonTsaiTW/LAT_Repo/blob/main/Mini_Hackathon/local_bread.py), [chatGPT相關程式碼 / chatGPT related codes](https://github.com/AndersonTsaiTW/LAT_Repo/blob/main/Mini_Hackathon/chatgptENG_cal.py), and [google map相關程式碼 / google map related codes](https://github.com/AndersonTsaiTW/LAT_Repo/blob/main/Mini_Hackathon/nearby_bakeries.py). 

### [ 目標使用者 / target user ]
<img width="1280" alt="Screenshot 2023-06-06 at 7 25 23 PM" src="https://github.com/AndersonTsaiTW/LAT_Repo/assets/113076298/c50219b9-d77f-4fbc-99fb-06aaadc00451">  
  
### [ 使用者操作流程 / User Operation Process ]
<img width="1280" alt="Screenshot 2023-06-06 at 7 25 59 PM" src="https://github.com/AndersonTsaiTW/LAT_Repo/assets/113076298/73046b88-4956-4f81-abb3-01b2518af65f">  
  
### [ 技術架構 / technical structure ]  
<img width="1280" alt="Screenshot 2023-06-06 at 7 26 41 PM" src="https://github.com/AndersonTsaiTW/LAT_Repo/assets/113076298/7fb60aef-4370-4ff6-88cc-632c082668d5">  
  
### [ QR code ]：如果你想實際測試，請聯絡製作團隊 / If you want to actually test it, please contact the production team  
![BreadExplorerQRcode](https://github.com/AndersonTsaiTW/LAT_Repo/assets/113076298/7355e154-e0fc-40c3-a6b6-1cc938665c14)

### 如果你想自己玩玩看 / if you want to play for yourself
0. 如果AZURE模型已失效，則無法測試 / Cannot test if the AZURE model is dead 
1. 下載資料夾程式碼 / Download the folder code
2. 建立自己的line頻道，取得token及secret，取得google map api的token，都寫入config.py中 / Create your own line channel, get the token and secret, get the token of google map api, and write them into config.py
3. 取得自己的openAI API token，在同一個資料夾建立 key.txt，直接寫入 / Obtain your own openAI API token, create key.txt in the same folder, and write directly
4. 啟動ngrok，本地port使用3001(./ngrok http 3001)，將網址更新到line頻道 / Start ngrok, use 3001 (./ngrok http 3001) for the local port, and update the URL to the line channel
5. 啟動 Bread_Explorer.py 主程式 / Start the main program: Bread_Explorer.py
6. 與lineBOT對話  / chat with lineBOT

#### 感謝您對本專案的關注，如果您對本專案有任何看法或是意見，請不吝惜向製作團隊提供意見。感謝。 / Thank you for your attention to this project. If you have any views or comments on this project, please feel free to provide comments to the production team. grateful. (e-mail: AndersonTsaiTW@gmail.com)

