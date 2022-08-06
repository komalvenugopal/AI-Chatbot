import json
json_data=open('files/questions.json', 'r')
data=dict(json.load(json_data))
d=data.copy()

while(True):
    try:
        d=d["questions"]
        print(d,"\n","\n")
        s=input()
        d=d[s]
        
    except:
        print(d["answer"])
        break


