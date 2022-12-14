import random
import json
import logging
import torch
import os
from model import NeuralNet
from utils import bag_of_words, tokenize, get_intents, mysqlselect

log = logging.getLogger(__name__)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
FILE = "files/data.pth"
data = torch.load(FILE)

model_state = data["model_state"]
input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Jivox"
intents=get_intents()

def get_response(msg):
    log.info("Recived Message: %s",msg)
    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)
    output = model(X)
    _, predicted = torch.max(output, dim=1)
    
    response={}
    tag = tags[predicted.item()]    
    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                response["tag"]= tag
                response["answer"]=random.choice(intent['responses'])                
                log.info(response)
                return response
    else:
        response["tag"]= ""
        response["answer"]="I do not understand..."
    return response


if __name__ == "__main__":
    print("Let's chat! (type 'quit' to exit)")
    while True:
        sentence = input("Hi, How can I help you: ")
        if sentence == "quit":
            break
        resp = get_response(sentence)
        print(resp)