import openai
keyfile = open("C:/Python36/Mini_Hackathon(0523_ok)/key.txt", "r")
# "C:\Python36\Mini_Hackathon(0523可執行) - 複製"
key = keyfile.readline()
openai.api_key = key

def chatgptfn(sub_list):
    print(sub_list)
#    result = ''
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant"},
            {"role": "user", "content": f"{sub_list} :請介紹這個東西的歷史故事、產地、文化意涵等內容，並提供繁體中文及英文版本。"},
        #    {"role": "assistant", "content": "Bread is a food of great historical significance and cultural value in the West"}
 
        ]
    )
    #for choice in response.choices:
    #    result += choice.message.content
    return response

    #Input a paragraph into ChatGPT and display the returned summary
#for i in range(20,len(data)):
#    data[i] = chatgptfn(data[i])
#    print(i)
#    print(data[i])
#
# print(chatgptfn("pineapple bun"))