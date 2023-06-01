import openai
keyfile = open("key.txt", "r")
# "C:\Python36\Mini_Hackathon(0523可執行) - 複製"
key = keyfile.readline()
openai.api_key = key

#導入麵包清單，如果不在清單裡面，則根本不送到chatGPT
import config
#print(config.breadlist)

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
        return response
    else:
        return "很抱歉，無法識別您所輸入的圖片。"



print(chatgptfn("pineapple_bun"))
#print(chatgptfn("天天開心"))