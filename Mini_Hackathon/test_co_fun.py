import chatgptENG
print(chatgptENG.chatgptfn("pineapple bun"))
print(chatgptENG.chatgptfn("pineapple bun").choices[0].message.content)

#import json
#with open("config.json") as f:
#    p = json.load(f)
#    print(p)

