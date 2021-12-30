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
    ![Create User Improved Interface](/screenshots/create_user_current.png)
    ![Send mail Improved Interface](/screenshots/send_mail_current.png)

    #TODO and future implementation
    1. TODO: Icon of the mail services in create user interface
    2. TODO: Auto fill of mail servicename(only for services which we support)
    3. TODO: Service id of the mail services(used by backend in pip package)
    4. FI: More editing options in message part in Send mail interface
    5. FI: Complete Dashboard of user(some mail services allow recieving of email also, dashboard can show all email from all providers in 1 place) 


 