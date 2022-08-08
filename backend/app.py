import json
import yaml
import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from utils import push_interaction
from utils import mysqlselect,get_intents,check_user
from chat import get_response
from reco import get_question_recommendation

app = Flask(__name__)
CORS(app,resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/reco/predict", methods=['GET','POST'])
def predict():
    try:
        body=request.get_json()
        args= dict(request.args)
        text = body.get("message")
        response = get_response(text)

        tag=response["tag"]
        userid=args["userid"]

        if(check_user(userid)==False):
            return "User Doesnt Exist"

        push_interaction(tag,userid)        
        if(tag!=""):
            answer=mysqlselect("select id from `eam_brb_tmp`.QUESTION where tag="+"'"+tag+"'")
            # log.info('Answer: ', answer[0][0])
            recommendations= get_question_recommendation(answer[0][0])
            message = {"answer": response["answer"],"recommendations":recommendations}
            log.info('Posted the answer %s', message)
            return jsonify(message)
        else:
            message = {"answer": response["answer"],"recommendations":get_question_recommendation(1)}
            log.info('Didnt find the answer %s', message)
            return jsonify(message)
        
    except Exception as e:
        app.logger.critical(e)

if __name__=="__main__":
    # logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    logging.basicConfig(filename='support.log', filemode='a', level=logging.INFO)
    log = logging.getLogger(__name__)
    log.info("Starting the application...")
    app.logger.debug("The application is getting started")
    app.run(host="0.0.0.0",port=5000, debug=True)
    log.critical("Application is Stopped...")
