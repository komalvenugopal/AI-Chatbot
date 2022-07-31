import yaml
import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from chat import get_response

app = Flask(__name__)
CORS(app)

with open("properties.yaml", "r") as config:
    config=yaml.safe_load(config)

@app.post("/predict" )
def predict():
    text = request.get_json().get("message")
    response = get_response(text)
    message = {"answer": response}
    log.info('Posted the response %s', message)
    return jsonify(message)

if __name__=="__main__":
    # logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    logging.basicConfig(filename='support.log', filemode='w', level=logging.INFO)
    log = logging.getLogger(__name__)
    log.info("Starting the application...")
    app.logger.debug("The application is getting started")
    app.run()
    log.critical("Application is Stopped...")