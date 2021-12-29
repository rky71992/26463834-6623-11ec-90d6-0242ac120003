import React, { Component } from 'react'
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import AppBar from 'material-ui/AppBar'  
import TextField from 'material-ui/TextField';
import RaisedButton from 'material-ui/RaisedButton';

export class UserCreate extends Component {

    continue = e => {
        e.preventDefault();
        this.props.nextStep();
    }

    createNewUser = e => {
        const {values} = this.props
        fetch('http://localhost:8000/createUser', {
        method: 'POST',
        headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json'
          },
        body: JSON.stringify({
            "userId": values.userId,
            "password": values.password,
            "sendgridApiKey": values.sendgridApiKey,
            "mailgunApiKey": values.mailgunApiKey,
            "mandrillApiKey": values.mandrillApiKey,
            "amazonApiKey": values.amazonApiKey
        })
        });
        console.log("Is this POST func running")
    }

    render() {
        const {values, handleChange} = this.props; 
        return (
            <MuiThemeProvider>
                <React.Fragment>
                    <AppBar title = "Create User"/>
                    <TextField
                        floatingLabelText = "New user ID"
                        onChange = {handleChange('userId')}
                    />
                    <br/>
                    <TextField
                        floatingLabelText = "Password"
                        onChange = {handleChange('password')}
                    />
                    <br/>
                    <TextField
                        floatingLabelText = "SendGrid API Key"
                        onChange = {handleChange('sendgridApiKey')}
                    />
                    <br/>
                    <TextField
                        floatingLabelText = "Mailgun API Key"
                        onChange = {handleChange('mailgunApiKey')}
                    />
                    <br/>
                    <TextField
                        floatingLabelText = "Mandrill API Key"
                        onChange = {handleChange('mandrillApiKey')}
                    />
                    <br/>
                    <TextField
                        floatingLabelText = "Amazon SUS API Key"
                        onChange = {handleChange('amazonApiKey')}
                    />
                    <br/>
                    <RaisedButton
                        label= "Submit"
                        primary = {true}
                        onClick={this.createNewUser}
                    />
                    <RaisedButton
                        label= "Skip"
                        primary = {true}
                        onClick={this.continue}
                    />
                </React.Fragment>
            </MuiThemeProvider>
        )
    }
}

export default UserCreate
