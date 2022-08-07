import yaml
import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from chat import get_response
from reco import get_question_recommendation
from utils import mysqlselect,get_intents

app = Flask(__name__)
CORS(app)

with open("properties.yaml", "r") as config:
    config=yaml.safe_load(config)

@app.post("/predict")
def predict():
    body=request.get_json()
    args= dict(request.args)
    text = body.get("message")
    response = get_response(text)
    tag=response["tag"]
    s=mysqlselect("select id from `eam_brb`.QUESTION where tag="+"'"+tag+"'")
    recommendations= get_question_recommendation(s[0][0])
    # message = {"answer": response["answer"]}
    message = {"answer": response["answer"],"recommendations":recommendations}
    log.info('Posted the response %s', message)
    return jsonify(message)

if __name__=="__main__":
    # logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    logging.basicConfig(filename='support.log', filemode='w', level=logging.INFO)
    log = logging.getLogger(__name__)
    get_intents()
    log.info("Starting the application...")
    app.logger.debug("The application is getting started")
    app.run()
    log.critical("Application is Stopped...")
