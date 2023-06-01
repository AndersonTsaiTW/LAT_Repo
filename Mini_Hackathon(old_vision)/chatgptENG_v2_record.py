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

def chatgptfn(sub_list):
    #進行麵包種類是否在清單中的判斷
    if sub_list in config.breadlist:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant"},
                {"role": "user", "content": f"{sub_list} :請介紹這個麵包的(1)歷史故事、(2)產地與文化意涵、(3)製作方式等內容，並提供中文及英文版本。"},
            #    {"role": "assistant", "content": "Bread is a food of great historical significance and cultural value in the West"}
    
            ]
        )
        print(response)
        return response.choices[0].message.content
    else:
        return "很抱歉，無法識別您所輸入的圖片。"


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



#print(chatgptfn("pineapple_bun"))
#print(chatgptfn("天天開心"))