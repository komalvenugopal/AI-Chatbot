# from ast import pattern
from urllib import response
import numpy as np
import nltk
from nltk.stem.porter import PorterStemmer
import json, string
from torch import rand
import pymysql,ast,logging,yaml

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')

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

from nltk.stem import WordNetLemmatizer 
from nltk.corpus import wordnet
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.corpus import wordnet

en_stops = set(stopwords.words('english')) 
punc=list(string.punctuation)
ignore_words=list(en_stops)+list(punc)

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

def push_interaction(tag,userid):
    questionid=""
    if(tag!=""):
        questionid=mysqlselect("select id from `eam_brb_tmp`.QUESTION where tag='{}'".format(tag))
        questionid=int(questionid[0][0])
        userid=int(userid)
        mysqlinsert("insert into `eam_brb_tmp`.CHATBOT_INTERACTIONS (user_id,question_id) values(%s,%s)",(userid,questionid))
        log.info("Pushed the interaction: %s, %s", userid,questionid)
    return "Pushed"

def check_user(userid):
    if(userid!=""):
        user_id=mysqlselect("select id from `eam_brb_tmp`.PERSON where ID='{}'".format(userid))
    if(len(user_id)==0):
        return False
    return True



# for i in range(1000):
#     from random import randint
#     mysqlinsert("insert into `eam_brb_tmp`.CHATBOT_INTERACTIONS (user_id,question_id) values(%s,%s)",(randint(1,50),randint(1,71)))

# push_interaction({"userid":1,"question_id":2})

# f=open("files/intents.json", "r")
# data=dict(json.load(f))["intents"]
# for i in data:
#     i["tag"]=i["patterns"][0].replace(" ","_")
#     push_intents(i)
#train the model after changing it    

# while(True):
#     import json
#     m=input("Question: ")
#     s=input("Response: ")[:230]
#     l=input("URL: ")
#     d={}
#     n=m.replace(" ","_")
#     d["tag"]=n
#     d["patterns"]=[m]
#     d["responses"]=[s+l]
#     print(push_intents(d))

#push shouldnt have ',",min of (1) val  
#max chars 1000

# d={}
# a=get_intents()
# for i in a["intents"]:
#     d[i["patterns"][0]]=dict({"answer":i["responses"][0]})

# print(json.dumps(d,indent=4))    
