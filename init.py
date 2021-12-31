import os
import json
import sys
import flask
import logging
from constants import *
from utils import *
from pymongo import MongoClient
from flask import request, jsonify, redirect
from flask_cors import CORS

LOG_FILE_PATH = "/home/rohit/Logs/aus_mail_service_logs.log"
logging.basicConfig(filename= LOG_FILE_PATH, format='%(asctime)s %(message)s' ,level=logging.DEBUG, force=True)
app = flask.Flask(__name__)
CORS(app)

#Local db conn
try:
    client=MongoClient()
    client = MongoClient('mongodb://localhost:27017/')
    db = client['aus_mail_service']
except Exception as ex:
    logging.fatal("Unable to connect to DB. Error: %s", str(ex))
    sys.exit()

@app.route("/createUser", methods=['POST'])
def create_new_user():
    '''
    This function creates new user along with different mail services API keys and saves in DB. If some new mail service is requested, it notifies the admin.
    '''
    return_msg = {}
    return_msg["Status"] = IN_PROGRESS
    return_msg["Message"] = ""
    
    new_user_info = json.loads(request.data)
    if not new_user_info:
        return_msg["Status"] = FAILED
        return_msg["Message"] = "No data passed in body"
        return return_msg , 400
    
    new_userid = str(new_user_info.get("userId","")).strip()
    new_user_password = str(new_user_info.get("password","")).strip()
    if (not new_userid) or (not new_user_password):
        return_msg["Status"] = ERROR
        return_msg["Message"] = "Username/Password cannot be empty"
        return return_msg, 400
    
    logging.debug("New user create request recieved with userID: %s",new_userid)
    
    #checking if userid is available
    if db["users"].find_one({"user_id":new_userid}):
        return_msg["Status"] = ERROR
        return_msg["Message"] = "User ID already exists"
        logging.debug("UserId: %s already exists. Not creating new user with this ID", new_userid)
        return return_msg, 400
    
    #this dict will be saved in DB
    new_user_data = {}
    new_user_data["user_id"] = new_userid
    new_user_data["password"] = md5_hash(new_user_password)
    
    mail_services_opted = []
    new_services_requested = []
    mail_services_opted, new_services_requested = format_mail_services_opted(new_user_info.get("services",[]))
    
    #mail_opted_services should be encrypted and then saved
    new_user_data["services"] = mail_services_opted
    
    #complete new user info have been generated, saving it to db
    db["users"].insert_one(new_user_data)
    logging.debug("New user create request processed and user inserted in DB. userID: %s", new_userid)
    
    #TODO: if users requested some new mail services which is not supported by us till now, if will be new_services_requested
    if new_services_requested:
        #send notification to admin or log it, so it can be noted and implemented in future
        pass 
    
    #NOTE: At this point, if user will know that a new user is created, however, he doesnot know that new_services_requested is not added to its
    #       account as those are not supported. A general meaage should be shown that these services will be supported in future
    return_msg["Status"] = SUCCESS
    return_msg["Message"] = "New user created"
    return return_msg
    

@app.route("/sendMail", methods=['POST'])
def send_mail():
    '''
    Sends the mail using mail services opted by user
    '''
    return_msg = {}
    return_msg["Status"] = IN_PROGRESS
    return_msg["Message"] = ""
    return_msg["Info"] = []

    new_mail_data = json.loads(request.data)
    
    user_id = str(new_mail_data.get("userId","")).strip()
    user_password = str(new_mail_data.get("password","")).strip()
    logging.debug("New mail send request recieved from user: %s",user_id)
    
    if not user_id or user_password:
        logging.debug("Cannot send mail without username and password")
        return_msg["Status"] = ERROR
        return_msg["Message"] = "Cannot send mail without username and password"
        return return_msg, 400 
        
    #checking if the user exists
    user_db_info = db["users"].find_one({"user_id":user_id, "password":md5_hash(user_password)})
    if not user_db_info:
        logging.debug("User doesnot exists. Cannot send mail without signup")
        return_msg["Status"] = ERROR
        return_msg["Message"] = "Cannot send mail without signup"
        return return_msg, 400
    
    mail_recepients = new_mail_data.get("to")
    subject = new_mail_data.get("subject","")
    message = new_mail_data.get("message","")
    if not (mail_recepients) or (not subject) or (not message):
        logging.debug("Cannot process if no mail_recipienst/subject/message provided")
        return_msg["Status"] = ERROR
        return_msg["Message"] = "mail_recipienst/subject/message required"
        return return_msg, 400
        
    user_opted_services = user_db_info.get("services")
    if not user_opted_services:
        logging.debug("Cannot send mail without any mail services opted.")
        return_msg["Status"] = FAILED
        return_msg["Message"] = "Cannot send mail without any mail services opted."
        return return_msg, 400
    
    try:
        ms = MailService(str(user_id))
        ms.add_service(user_opted_services)
        #print(ms.is_service_processed())
        ms.add_message(subject,message)

        exe_status = ms.mail_execute([mail_recepients])
    except Exception:
        raise
    
    #logging the services status
    for status in exe_status:
        logging.debug("Overall mail status to recipient %s is ::%s",status["to"],status["overall_status"])
        for mail_services in status["mail_service_status"]:
            if mail_services["status"] != SUCCESS:
                logging.warning("Mail service is down for service %s . Error::",mail_services["service_id"],mail_services.get("error"))
                
    return_msg["Info"] = exe_status
    return_msg["Status"] = SUCCESS
    return return_msg
    


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)