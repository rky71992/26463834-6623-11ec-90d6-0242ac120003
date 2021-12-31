#!/usr/bin/python3
import requests

class MailService(object):
    'This class sends mail using different services'
    valid_mail_service_id = ['sendgrid','mailgun','mandrill','amazon']
    NOT_STARED = "not_started"
    SUCCESS = "success"
    FAILED = "failed"
    
    def __init__(self, service_obj_name):
        self.service_obj_name = service_obj_name
        self.mail_service = []
        self.service_processed = False
        self.message = ""
        self.subject = ""
        self.recipients = []
    
    def add_service(self,mail_service_list):
        if not isinstance(mail_service_list,list):
            raise TypeError("add_service accepts list containg services dict. Invalid argument passed")
        
        for service in mail_service_list:
            if not isinstance(service,dict):
                raise TypeError("service is of type dict expected. some other value passed")
            
            service_id = str(service.get("id","")).strip()
            service_key = str(service.get("key","")).strip()
            
            if (not service_id) or service_id not in MailService.valid_mail_service_id:
                raise NotImplementedError("Service for service id: %s is not implemented",format(service_id))
            if not service_key:
                raise ValueError("Invalid key passed")
            
            self.mail_service.append({"id":service_id,"key":service_key})
    
    def is_service_processed(self):
        return self.service_processed
    
    def add_message(self,subject,message):
        if not isinstance(subject,str):
            raise TypeError("subject must be of type string. %s passed",format(type(subject)))
        if not isinstance(message,str):
            raise TypeError("message must be of type string. %s passed",format(type(message)))
        self.subject = subject
        self.message = message
    
    def __validate_mail_execute(self, recipients_list):
        if self.service_processed:
            raise Exception("Mail service already called. Cannot call again.")
        
        if self.mail_service == []:
            raise ValueError("add mail service first by calling add_service(mail_service_list)")
        
        if not isinstance(recipients_list,list):
            raise TypeError("mail_execute requires list of recipeints. %s passed",format(type(recipients_list)))
        
        for recipient in recipients_list:
            if not isinstance(recipient,str):
                raise TypeError("recipient type must be string. %s passed",type(recipient))
    
    def __send_mail_using_sendgrid(self,key,message_info):
        return_msg = {}
        return_msg["status"] = ""
        return_msg["error"] = ""
        sendgrid_mail_send_url = "https://api.sendgrid.com/api/mail.send.json"
        header = {"Authorization": "Bearer "+ key}

        payload = {}
        payload["to"] = message_info["to"]
        payload["subject"] = message_info["subject"]
        payload["from"] = message_info["from"]
        payload["text"] = message_info["message"]
        
        try:
            r = requests.post(url=sendgrid_mail_send_url ,headers=header,data=payload)
        except Exception as ex:
            return_msg["status"] = MailService.FAILED
            return_msg["error"] = str(ex)
            return return_msg
        
        if r.status_code == 200:
            return_msg["status"] = MailService.SUCCESS
        
        return return_msg
    
    def __send_mail_using_mailgun(self,key,message_info):
        return {"status":"failed","error":"Not implemented"}
    
    def __send_mail_using_mandrill(self,key,message_info):
        return {"status":"failed","error":"Not implemented"}
        pass
    
    def __send_mail_using_amazon(self,key,message_info):
        return {"status":"failed","error":"Not implemented"}
        pass
    
    def mail_execute(self,recipients_list):
        MailService.__validate_mail_execute(self,recipients_list)
        self.service_processed = True

        return_info = []
        for recipient in recipients_list:
            #from is hardcoded for now, it will be senders email address
            msg = {"from":"rky71992@gmail.com","to":recipient,"subject":self.subject,"message":self.message}
            temp_dict = {}
            temp_dict["to"] = recipient
            temp_dict["overall_status"] = False
            mail_service_status = []
            for service in self.mail_service:
                if service["id"] == 'sendgrid':
                    send_status = MailService.__send_mail_using_sendgrid(self, key= service["key"],message_info=msg)
                    mail_service_status.append({"service_id":service["id"],"status":send_status["status"],"error":send_status["error"]})
                    if send_status["status"] == MailService.FAILED:
                        continue
                    if send_status["status"] == MailService.SUCCESS:
                        temp_dict["overall_status"] = True
                        break
                        
                elif service["id"] == 'mailgun':
                    send_status = MailService.__send_mail_using_mailgun(self, key= service["key"],message_info=msg)
                    mail_service_status.append({"service_id":service["id"],"status":send_status["status"],"error":send_status["error"]})
                    if send_status["status"] == MailService.FAILED:
                        continue
                    if send_status["status"] == MailService.SUCCESS:
                        temp_dict["overall_status"] = True
                        break
                    
                elif service["id"] == 'mandrill':
                    send_status = MailService.__send_mail_using_mandrill(self, key= service["key"],message_info=msg)
                    mail_service_status.append({"service_id":service["id"],"status":send_status["status"],"error":send_status["error"]})
                    if send_status["status"] == MailService.FAILED:
                        continue
                    if send_status["status"] == MailService.SUCCESS:
                        temp_dict["overall_status"] = True
                        break
                    
                elif service["id"] == 'amazon':
                    send_status = MailService.__send_mail_using_amazon(self, key= service["key"],message_info=msg)
                    mail_service_status.append({"service_id":service["id"],"status":send_status["status"],"error":send_status["error"]})
                    if send_status["status"] == MailService.FAILED:
                        continue
                    if send_status["status"] == MailService.SUCCESS:
                        temp_dict["overall_status"] = True
                        break
            
            temp_dict["mail_service_status"] = mail_service_status
            return_info.append(temp_dict)
        
        return return_info
            
            
ms = MailService("personal")
ms.add_service([{"key":"afsafafaf","id":"sendgrid"},{"key":"afsafafaf","id":"mailgun"}])
print(ms.is_service_processed())
ms.add_message("This is sub","This is message")

exe_status = ms.mail_execute(["rohit@gmail.com"])
print(exe_status)
        
        
    
    
        
        