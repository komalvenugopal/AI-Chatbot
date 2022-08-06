import random
import json
import logging
import torch

from model import NeuralNet
from utils import bag_of_words, tokenize


import os
print(os.getcwd())

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
with open('files/intents.json', 'r') as json_data:
    intents = json.load(json_data)

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

def get_response(msg):
    log = logging.getLogger(__name__)
    log.info("Recived Message: %s",msg)
    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                return random.choice(intent['responses'])
    
    return "I do not understand..."


if __name__ == "__main__":
    print("Let's chat! (type 'quit' to exit)")
    while True:
        sentence = input("Hi, How can I help you: ")
        if sentence == "quit":
            break

        resp = get_response(sentence)
        print(resp)