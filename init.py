import os
import json
import flask
import logging
from flask import request, jsonify, redirect
from flask_cors import CORS

LOG_FILE_PATH = "/home/rohit/Logs/aus_mail_service_logs.log"
logging.basicConfig(filename= LOG_FILE_PATH, format='%(asctime)s %(message)s' ,level=logging.DEBUG, force=True)
app = flask.Flask(__name__)
CORS(app)


@app.route("/createUser", methods=['POST'])
def create_new_user():
    '''
    This function takes list as input, and evaluates the similarity between model_answer and student_answer
    More data listed in API_documentation file
    '''

    user_info = json.loads(request.data)
    print(user_info)
    return { "Status": True}

@app.route("/sendMail", methods=['POST'])
def send_mail():
    '''
    This function takes list as input, and evaluates the similarity between model_answer and student_answer
    More data listed in API_documentation file
    '''

    user_info = json.loads(request.data)
    print(user_info)
    return { "Status": True}

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)