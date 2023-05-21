import chatgptENG
#print(chatgptENG.chatgptfn("pineapple bun"))

import json
with open("config.json") as f:
    p = json.load(f)
    print(p)

