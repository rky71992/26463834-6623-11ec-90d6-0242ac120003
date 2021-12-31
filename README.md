# Email Service API
 
 Problem Statement
    1. Create an email pip package, which can be open source and reuseable in any other services.
        The package should provide an abstraction between multiple email service providers.
        If one of the services goes down, it can quickly failover to a another provider without affecting your customers.

    2. Create a RESTful API that accepts the necessary information and sends emails via the created pip package, if you like, you can build a UI to use that    RESTful API.

# UI 

    #Package Dependencies
    1. npm - (apt install npm)- This will also innstall node.js
    2. create-react-app utility (npm -g install create-react-app)
    3. Material-ui (npm i material-ui)

    #Starting the project
    1. To start the UI, run "npm start" in emailserviceui directory.
    2. By default a new browser window will open pointing http://locathost:3000, if not opened by default open this link manually.
    3. NOTE: If port 3000 is used by some other services, react will jump to the next open port(3001)

    #Screenshots
    ![Create User Interface](/screenshots/create_user_current.png)
    ![Send mail Interface](/screenshots/send_mail_current.png)

    #How can be improved
    ![Create User Improved Interface](/screenshots/create_user_improved.png)
    ![Send mail Improved Interface](/screenshots/send_mail_improved.png)

    #TODO and future implementation
    1. TODO: Icon of the mail services in create user interface
    2. TODO: Auto fill of mail servicename(only for services which we support)
    3. TODO: Service id of the mail services(used by backend in pip package)
    4. FI: More editing options in message part in Send mail interface
    5. FI: Complete Dashboard of user(some mail services allow recieving of email also, dashboard can show all email from all providers in 1 place) 
    6. TODO: Show created sucessfully/ mail sent message to user on user create interface/send mail interface

# Backend

    Backend is coded in python. Microservices are user as the project is small
    #Package Dependencies
    1. Python3
    2. flask
    3. flask_cors
    4. pymongo
    5. mongodb


    # API documentation
    ############################################################################################################################################
    NOTE: 
        1. user passwords are saved using md5 hash +salt
    #TODO and future implementation
        1. TODO: mail api keys are saved in plain text, should be encrypted and saved
        2. FI: add /updateUser and /deleteUser for user updation
        3. TODO: when a new mail service is requested, notify admin about requested service

    @app.route("/createUser", methods=["POST"])
        This function creates new user along with different mail services API keys and saves in DB. If some new mail service is requested, it notifies the admin.

        Input:{
            "userId": Required
            "password": Required
            "services:[{"service_id":"mailgun","key":"mailgun API key"}] Optional
        }

        Output:
        {
            return_msg["Status"] = SUCCESS
            return_msg["Message"] = "New user created"
        }

        Cases:
            1. If no data is sent
                Output: {                                       Status Code: 400
                        "Status" = "Failed"
                        "Message" = "No data is passed in body"
                        }
            2. If no username/password
                Output: {                                       Status Code: 400
                        "Status" = "Error"
                        "Message" = "Username/Password cannot be empty"
                        }
            3. If userid already exists
                Output: {                                       Status Code: 400
                        "Status" = "Failed"
                        "Message" = "User ID already exists"
                        }
            4. Unknown error
                Status code: 500
    
    ###################################################################################################################################################
    #TODO and future implementation
        1. TODO: currently "to" key in input is string, list should be there
        2. FI: add more functionality of messages
    
    @app.route("/sendMail", methods=["POST"])
        This function creates new user along with different mail services API keys and saves in DB. If some new mail service is requested, it notifies the admin.

        Input:{
            "userId": Required
            "password": Required
            "to": "" Required
            "subject": "" required
            "message": ""  Required
        }

        Output:
        {
            return_msg["Status"] = SUCCESS
            return_msg["Message"] = ""
            "info":[    {"to": "rohit@gmail.com",
                         "overall_status": True, 
                         "mail_service_status": 
                            [{  "service_id": "sendgrid",
                                "status": "failed",
                                "error": "Some error in sendgrid"
                            }, 
                                {"service_id": "mailgun", 
                                "status": "success", 
                                "error": ""
                            }]}]
        }

        Cases:
            1. If no userid/password
                Output: {                                       Status Code: 400
                        "Status" = "Error"
                        "Message" = "Cannot send mail without username and password"
                        "info": []
                        }
            2. If invalid user
                Output: {                                       Status Code: 400
                        "Status" = "Error"
                        "Message" = "Cannot send mail without signup"
                        "info": []
                        }
            3. If no mail services were added during Create user
                Output: {                                       Status Code: 400
                        "Status" = "Failed"
                        "Message" = "Cannot send mail without any mail services opted."
                        "info": []
                        }
            3. If no to,subject,message:
                Output: {                                       Status Code: 400
                        "Status" = "Failed"
                        "Message" = "mail_recipienst/subject/message required"
                        "info": []
                        }
            4. Unknown error
                Status code: 500

# PIP package