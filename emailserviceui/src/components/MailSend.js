import React, { Component } from 'react'
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import AppBar from 'material-ui/AppBar'  
import TextField from 'material-ui/TextField';
import RaisedButton from 'material-ui/RaisedButton';

export class MailSend extends Component {

    back = e => {
        e.preventDefault();
        this.props.prevStep();
    }

    sendNewMail = e => {
        const {values} = this.props
        fetch('http://localhost:8000/sendMail', {
        method: 'POST',
        headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json'
          },
        body: JSON.stringify({
            "userId": values.userId,
            "password": values.password,
            "to": values.mailReciever,
            "subject": values.mailSubject,
            "message": values.mailMessage,
        })
        });
        console.log("Is mail sending POST working")
    }

    render() {
        const {values, handleChange} = this.props; 
        return (
            <MuiThemeProvider>
                <React.Fragment>
                    <AppBar title = "Send Mail"/>
                    <TextField
                        floatingLabelText = "User ID"
                        onChange = {handleChange('userId')}
                    />
                    <br/>
                    <TextField
                        floatingLabelText = "Password"
                        onChange = {handleChange('password')}
                    />
                    <br/>
                    <TextField
                        floatingLabelText = "To"
                        onChange = {handleChange('mailReciever')}
                    />
                    <br/>
                    <TextField
                        floatingLabelText = "Subject"
                        onChange = {handleChange('mailSubject')}
                    />
                    <br/>
                    <TextField
                        floatingLabelText = "Message"
                        multiLine
                        rows={4}
                        onChange = {handleChange('mailMessage')}
                    />
                    <br/>
                    <RaisedButton
                        label= "Back"
                        primary = {true}
                        onClick={this.back}
                    />
                    <RaisedButton
                        label= "Send"
                        primary = {true}
                        onClick={this.sendNewMail}
                    />
                </React.Fragment>
            </MuiThemeProvider>
        )
    }
}

export default MailSend
