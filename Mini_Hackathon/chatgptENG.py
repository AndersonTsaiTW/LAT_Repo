import openai
import pandas as pd
keyfile = open("/Users/anderson/Desktop/Data Science/OpenAI/key.txt", "r")
key = keyfile.readline()
openai.api_key = key

def chatgptfn(sub_list):
    result = ''
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant"},
            {"role": "user", "content": f"{sub_list} :give me a summary"},
            {"role": "assistant", "content": "Bread is a food of great historical significance and cultural value in the West"}
 
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

#print(chatgptfn("pineapple bun"))