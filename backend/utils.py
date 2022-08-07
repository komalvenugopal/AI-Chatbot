# from ast import pattern
from urllib import response
import numpy as np
import nltk
from nltk.stem.porter import PorterStemmer
import json
from torch import rand
import pymysql,ast,logging,yaml

stemmer = PorterStemmer()
log = logging.getLogger(__name__)

config_file=open("properties.yaml", "r")
config=yaml.safe_load(config_file)

conn = pymysql.connect(
        host=config["db"]["host"],
        # host='db.dev.jivox.com',
        user=config["db"]["username"],
        password = config["db"]["password"])

def tokenize(sentence):
    return nltk.word_tokenize(sentence)


def stem(word):
    return stemmer.stem(word.lower())


def bag_of_words(tokenized_sentence, words):
    sentence_words = [stem(word) for word in tokenized_sentence]
    bag = np.zeros(len(words), dtype=np.float32)
    for idx, w in enumerate(words):
        if w in sentence_words: 
            bag[idx] = 1
    return bag

def mysqlselect(s):
    try:
        cur = conn.cursor()
        cur.execute(s)
        output = cur.fetchall()
        conn.commit()
        return output
    except Exception as e:
        print(e)
        conn.close()    

def mysqlinsert(s,args):
    try:
        cur = conn.cursor()
        cur.execute(s,args)
        output = cur.fetchall()
        conn.commit()
    except Exception as e:
        print(e)
        conn.close()


def get_intents():
    f=open("files/intents.json", "w")
    dict={"intents":[]}
    questions=mysqlselect("select * from `eam_brb_tmp`.QUESTION")
    for i in questions:
        temp={}
        temp["tag"]=i[1]
        temp["patterns"]= ast.literal_eval(i[2])
        temp["responses"]=ast.literal_eval(i[3])
        dict["intents"].append(temp)
    temp=json.dumps(dict,indent=4)
    f.write(temp)
    log.info("Created the questsions local file")
    json_data=open('files/intents.json', 'r')
    intents = json.load(json_data)
    return intents

def push_intents(data):
    tag= str(data ["tag"])
    pattern= json.dumps(eval(str(data ["patterns"])))
    responses=json.dumps(eval(str(data ["responses"])))
    args=(tag,pattern,responses)
    mysqlinsert("insert into `eam_brb_tmp`.QUESTION (tag,pattern,response) values(%s,%s,%s)",args)

def push_interaction():
    
    return

# f=open("files/intents.json", "r")
# data=dict(json.load(f))["intents"]
# for i in data:
#     i["tag"]=i["patterns"][0].replace(" ","_")
#     push_intents(i)
#train the model after changing it    

#push shouldnt have ',",min of (1) val  
#max chars 1000

# get_intents()