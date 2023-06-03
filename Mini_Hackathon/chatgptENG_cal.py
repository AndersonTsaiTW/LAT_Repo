import openai
keyfile = open("key.txt", "r")
# "C:\Python36\Mini_Hackathon(0523可執行) - 複製"
key = keyfile.readline()
openai.api_key = key

#導入麵包清單，如果不在清單裡面，則根本不送到chatGPT
import config
#print(config.breadlist) #檢查麵包類型讀取使用
import json
record_file = "Bread_chat.json"
import random

def chatgptfn(sub_list):
    #進行麵包種類是否在清單中的判斷
    if sub_list in config.bread_all:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant"},
                {"role": "user", "content": f"{sub_list} :請用中文介紹這個麵包的(1)歷史故事、(2)產地與文化意涵、(3)製作方式等內容，並提供英文翻譯。"},
            #    {"role": "assistant", "content": "Bread is a food of great historical significance and cultural value in the West"}
    
            ]
        )
        print(response)
        return response.choices[0].message.content
    else:
        return "很抱歉，我們不知道這是什麼麵包喔"


def breadchatrecord(bread_tag,chat_reply,rate):
    sub_list = bread_tag
    new_chat = [chat_reply,[rate]]
    with open(record_file, "r") as file:
        existing_data = json.load(file)
        # 檢查麵包類別是否已存在
        if sub_list in existing_data:
            # 將新的描述加入現有的類別中
            existing_data[sub_list].append(new_chat)
        else:
            # 若麵包類別不存在，則建立新的類別與描述
            existing_data[sub_list] = [new_chat]

    # 寫入更新後的資料至JSON檔案
    with open(record_file, "w") as file:
        json.dump(existing_data, file)

def fakegptfn(sub_list):
    #進行麵包種類是否在清單中的判斷
    if sub_list in config.breadlist:

        with open(record_file, "r") as file:
            existing_data = json.load(file)
            len_index = len(existing_data[sub_list])-1
            r = random.randint(0,len_index)
            #print(r)
            #print(len(existing_data[breadtag][r][0]))
            response = existing_data[sub_list][r][0]

        print(response)
        return response.choices[0].message.content
    else:
        return "很抱歉，我們不知道這是什麼麵包"

#print(chatgptfn("pineapple_bun"))
#print(chatgptfn("天天開心"))