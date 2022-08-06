import json


json_data=open('files/questions.json', 'r')
data=dict(json.load(json_data))

patterns=open('files/patterns.json', 'r')
patterns = json.load(patterns)

def qa_func(parent,data):
    if("questions" in data.keys()):
        keys=data['questions'].keys()
        for i in keys:
            qa_func(i,data["questions"][i])

    elif("answer" in data.keys()):
        parent_copy=parent.replace(" ","_")
        print(parent_copy)
        tempd={}
        tempd["tag"]=parent_copy
        tempd["patterns"]=[parent]
        tempd["responses"]=[data["answer"]]
        patterns["intents"].append(tempd)

def generate_intents():
    qa_func(None,data)
    intents=open('files/intents.json', 'w')
    json_object = json.dumps(patterns, indent = 4) 
    print(json_object)
    intents.write(json_object)

    