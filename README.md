# LAT_Repo  
###### (2023)Learning Analytics Tools in NTNU // 111-2 臺師大教育大數據微學程 
### 學習分析工具實務應用  
授課教師：蔡芸琤(Pecu)、鍾祥仁(Ryan)   
姓名：蔡昱宏(Anderson)  
系級：校外選讀生(Student and Teaching Assistant)  
Class Time：Wed. 15:30\~18:20  
TA時間：Every Thu. 9:10\~16:20 (lunch break 11:20\~13:10) in 2023/3\~2023/6  
Questions are welcome on the "issue" page 

## 課程筆記區(Notes)
#### 2023/3/15
Teach how to use OpenAI with [API](https://platform.openai.com/docs/guides/chat/introduction) and [Fine-Tuning](https://platform.openai.com/docs/guides/fine-tuning), you can also refer to teacher's code - [Pecu's reference](https://github.com/pecu/peculab/tree/main/ChatGPT)
#### 2023/3/29
TF-IDF, LDA model : [Pecu's reference](https://github.com/pecu/LAT/blob/main/HW3/TextMining.ipynb)
#### 2023/4/26
Use Microsoft AZURE Language Model and LineBot to build an simple test : [Link](https://github.com/AndersonTsaiTW/LAT_Repo/tree/main/Notes/AZURE%20Language%20model)  
[References](https://mobiledev.tw/language-service-hotel-review-bot/), [Use NodeJS](https://nodejs.org/zh-tw)


## 作業連結區(Homewroks)
#### HW1 - [Are private senior high schools better than public ones? - Data analysis of senior high schools in Taiwan.](https://github.com/AndersonTsaiTW/LAT_Repo/blob/main/HW1/HW1_HighSchool_Analysis.ipynb)  (Find an education-related material by yourself, ask 10 questions and answer them)
1. This study compares the data of senior high schools in Taiwan in 2014(The peak of the previous business cycle) and 2020(After the impact of covid-19).
2. Private schools have a higher teacher-student ratio than public schools in 2020.
3. After experiencing covid-19, the numbers of teachers and students have decreased significantly. Among them, private schools have experienced the most significant reduction, but the teacher-student ratio has improved.

#### HW2 - [Changes in Teacher-Student Ratio and Class Sizes in High School - from 2014 to 2010 in Taiwan.](https://github.com/AndersonTsaiTW/LAT_Repo/blob/main/HW2/HW2_HighSchool_Graph.ipynb)
* [nbviewer vision](https://nbviewer.org/github/AndersonTsaiTW/LAT_Repo/blob/main/HW2/HW2_HighSchool_Graph.ipynb)

#### HW3 - [Use ChatGPT and IDA Model to find the topic in recent Canada Education news](https://github.com/AndersonTsaiTW/LAT_Repo/blob/main/HW3/HW3_IDA_ChatGPT.ipynb)
* Search education news on CBC(Canadian Broadcasting Corporation) News and analyze the most popular 3 topic
* [nbviewer vision](https://nbviewer.org/github/AndersonTsaiTW/LAT_Repo/blob/main/HW3/HW3_IDA_ChatGPT.ipynb)
  
#### HW4 - [Customer Review Sentiment Analysis Bot](https://github.com/AndersonTsaiTW/LAT_Repo/tree/main/Notes/AZURE%20Language%20model)
* [the readme.md](https://github.com/AndersonTsaiTW/LAT_Repo/blob/main/Notes/AZURE%20Language%20model/readme.md): Documentation showing the results of program execution 
* Using line's virtual identity, combined with Azure's emotion discrimination and message topic extraction functions, automatically analyze customer feedback messages: [code](https://github.com/AndersonTsaiTW/LAT_Repo/blob/main/Notes/AZURE%20Language%20model/index.js)
* Combined with the JSON SERVER provided by AZURE, the analysis results are stored in the cloud, and plotly is used to make simple analysis charts: [code - html](https://github.com/AndersonTsaiTW/LAT_Repo/blob/main/Notes/AZURE%20Language%20model/index.html), [code - js](https://github.com/AndersonTsaiTW/LAT_Repo/blob/main/Notes/AZURE%20Language%20model/main.js)

## 專題連結區(end-of-semester project) - [麵包探險家(Bread Explorer)](https://github.com/AndersonTsaiTW/LAT_Repo/tree/main/Mini_Hackathon)
* 專案影片 / project video[(連結 / Link)](https://www.youtube.com/watch?v=8w7uTnBEiGQ&ab_channel=AndersonTsai)
* 專案說明投影片 / Project Description ppt [(連結 / Link)](https://drive.google.com/drive/folders/1O0YNpWWHMssmgJTJc4bRilS4C7HKuTLE)
* 專案成員 / Members: [數學113 蔡尚峰 / Shawn](https://github.com/Shawn0604)、[機電113 鍾孟霖](https://github.com/mlchung1231)、[選讀 蔡昱宏 / Anderson](https://github.com/AndersonTsaiTW)
* 指導老師 / Project advisor: 蔡芸琤 / Pecu、鍾祥仁 / Ryan
* 專案特色 / Project Features:  
專案特點：
  1. 協助華語學生學習日常生活中與麵包相關的英語。 / Assist Chinese-speaking students to learn English related to bread in daily life.
  2. 結合 LineBOT、AZURE、chatGPT 等軟件，打造隨時隨地為您提供幫助的 Line 好友。 / Combine LineBOT, AZURE, chatGPT and other software to create Line friends who can assist you wherever you go.
  3. 引入用戶反饋機制，讓服務持續自我優化。 / Introduce a user feedback mechanism so that the service can continue to self-optimize.
* [主程式資料夾 / Folder - Mini_Hackathon](https://github.com/AndersonTsaiTW/LAT_Repo/tree/main/Mini_Hackathon): You can find all the codes here (written in python), including the [主程式碼 / main code](https://github.com/AndersonTsaiTW/LAT_Repo/blob/main/Mini_Hackathon/Bread_Explorer.py), AZURE電腦視覺模型 / AZURE related codes: [url_bread](https://github.com/AndersonTsaiTW/LAT_Repo/blob/main/Mini_Hackathon/url_bread.py) and [local_bread](https://github.com/AndersonTsaiTW/LAT_Repo/blob/main/Mini_Hackathon/local_bread.py), [chatGPT相關程式碼 / chatGPT related codes](https://github.com/AndersonTsaiTW/LAT_Repo/blob/main/Mini_Hackathon/chatgptENG_cal.py), and [google map相關程式碼 / google map related codes](https://github.com/AndersonTsaiTW/LAT_Repo/blob/main/Mini_Hackathon/nearby_bakeries.py). 

* [ QR code ]：如果你想實際測試，請聯絡製作團隊 / If you want to actually test it, please contact us  
![BreadExplorerQRcode](https://github.com/AndersonTsaiTW/LAT_Repo/assets/113076298/7355e154-e0fc-40c3-a6b6-1cc938665c14)

#### 感謝您對麵包探險家(Bread Explorer)專案的關注，如果您有任何看法或是意見，請不吝惜向製作團隊提供意見。感謝。 / Thank you for your attention to this project. If you have any views or comments on this project, please feel free to provide comments to the production team. grateful. (e-mail: AndersonTsaiTW@gmail.com)

## 其他補充
