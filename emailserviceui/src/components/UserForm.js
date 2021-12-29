import React, { Component } from 'react'
import MailSend from './MailSend';
import UserCreate from './UserCreate';

export class UserForm extends Component {

    state = {
        step: 1,
        userId: "",
        password: "",
        sendgridApiKey: "",
        mailgunApiKey: "",
        mandrillApiKey: "",
        amazonApiKey: "",
        mailReciever: "",
        mailSubject: "",
        mailMessage: ""
    };

    //to next step
    nextStep = () => {
        const { step } = this.state;
        this.setState({
            step: step + 1
        });
    };

    //to previous step
    prevStep = () => {
        const { step } = this.state;
        this.setState({
            step: step - 1
        });
    };

    handleChange = input => e => {
        this.setState({[input]: e.target.value });
    };

    render() {
        const {step} = this.state;
        const {userId, password, sendgridApiKey, mailgunApiKey, mandrillApiKey,amazonApiKey,mailReciever, mailSubject, mailMessage } = this.state;
        const values = {userId, password, sendgridApiKey, mailgunApiKey, mandrillApiKey,amazonApiKey, mailReciever, mailSubject, mailMessage};

        switch(step) {
            case 1:
                return (
                    <UserCreate 
                    nextStep = {this.nextStep}
                    handleChange = {this.handleChange}
                    values = {values}
                    />
                );
            case 2:
                return (
                    <MailSend
                    nextStep={this.nextStep}
                    prevStep={this.prevStep}
                    handleChange={this.handleChange}
                    values={values}
                    />
                )

        }
    }
}

export default UserForm
