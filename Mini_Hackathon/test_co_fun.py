#import chatgptENG
#print(chatgptENG.chatgptfn("pineapple bun"))
#print(chatgptENG.chatgptfn("pineapple bun").choices[0].message.content)

#import json
#with open("config.json") as f:
#    p = json.load(f)
#    print(p)

#import brtestpr1
#print(brtestpr1.breadpredict("https://i.postimg.cc/xjkRY5jt/2.jpg"))

import json
#把資料寫入JSON裡面存起來
record_file = "Bread_chat.json"
sub_list = "baguette"
new_chat = ["baguette is good and delicious",[0]]


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


