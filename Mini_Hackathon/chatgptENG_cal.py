import openai
keyfile = open("key.txt", "r")
# "C:\Python36\Mini_Hackathon(0523可執行) - 複製"
key = keyfile.readline()
openai.api_key = key

import random

#print(config.breadlist) #檢查麵包類型讀取使用
import json
record_file = "Bread_chat.json"

#導入麵包清單，如果不在清單裡面，則根本不送到chatGPT
import config

def chatgptfn(sub_list):
    #進行麵包種類是否在清單中的判斷
    if sub_list in config.bread_all:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant"},
                {"role": "user", "content": f"{sub_list} :請用中文介紹這個麵包的(1)歷史故事、(2)產地與文化意涵、(3)製作方式等內容，提供英文翻譯。在開頭的地方用這個麵包的中文及英文做標題。"},
            #    {"role": "assistant", "content": "Bread is a food of great historical significance and cultural value in the West"}
    
            ]
        )
        print(response)
        return response.choices[0].message.content
    else:
        return "很抱歉，我們不知道這是什麼麵包喔"


def breadchatrecord(bread_tag,chat_reply,rate):
    #sub_list = bread_tag
    new_chat = [chat_reply,[rate]]
    with open(record_file, "r") as file:
        existing_data = json.load(file)
        # 檢查麵包類別是否已存在
        if bread_tag in existing_data:
            # 將新的描述加入現有的類別中
            existing_data[bread_tag].append(new_chat)
        else:
            # 若麵包類別不存在，則建立新的類別與描述
            existing_data[bread_tag] = [new_chat]

    # 寫入更新後的資料至JSON檔案
    with open(record_file, "w") as file:
        json.dump(existing_data, file)

def fakegptfn(sub_list):
    #fakeGPT是依照使用者回饋，把好的答案保留並重複發送的機制
    #進行麵包種類是否在清單中的判斷
    if sub_list in config.breadlist:

        with open(record_file, "r") as file:
            existing_data = json.load(file)

            weights = []
            for i in range(0,len(existing_data[sub_list])):
                w = max(0,sum(existing_data[sub_list][i][1]))
                weights.append(w)

            #total_sum = sum(weights)
            add_weights = []
            for j in range(len(weights)):
                if j == 0:
                    add_weights.append(weights[j])
                else:
                    add_weights.append(add_weights[j-1] + weights[j])
                
            total_sum = sum(weights)
            pro = [w / total_sum for w in add_weights]
            #print(pro)

            r = random.random()
            #print(r)
            index = 0
            while index < len(pro) and r > pro[index]:
                print(index)
                index += 1

            #print(index)
            #print(len(existing_data[breadtag][r][0]))
            response = existing_data[sub_list][index][0]

        #print(response)
        fake_reply = [total_sum, index, response]
        return fake_reply
    else:
        fake_reply = [0,0, "很抱歉，我們不知道這是什麼麵包"]
        return fake_reply

#紀錄fakeGPT回應的使用者評價
def breadfakerecord(bread_tag,index,rate):
    with open(record_file, "r") as file:
        existing_data = json.load(file)
    #依照麵包種類、第幾個答案，寫入顧客評價
    existing_data[bread_tag][index][1].append(rate)

    # 寫入更新後的資料至JSON檔案
    with open(record_file, "w") as file:
        json.dump(existing_data, file)

#print(chatgptfn("pineapple_bun"))
#print(chatgptfn("天天開心"))
#print(fakegptfn("pineapple_bun"))
#breadfakerecord("pineapple_bun",0,0)