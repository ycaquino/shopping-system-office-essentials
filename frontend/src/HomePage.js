import React, {Component, useState} from 'react';
import {Button, Container, Divider, Form, Grid, Header, Modal, Segment, Tab} from 'semantic-ui-react';
import axios from "axios";
import * as storeData from "store";
import "./Home.css";

function CheckingAuth() {
    if(typeof storeData.get('id') === 'undefined'){
        return (<HomePage />)
    }

    else {
        window.location = '/UserView'
    }

}


class HomePage extends Component {

    state = { email: '', password: '', emailNew: '', passwordNew:'', firstName: '', lastName:'',
        submittedEmail: '', submittedPassword: '', submittedFirstName: '', submittedLastName: '', submittedPhoneNum:'',
    }

    handleUserChange = (e, { name, value }) => this.setState({ [name]: value })

    handleNewUserChange = (e, { name, value }) => this.setState({ [name]: value })

    handleUserSubmit = () => {
        const { email, password } = this.state

        if(email === '' || password === ''){
            alert('Please enter both your email and password.')
        } else {
            this.setState({ submittedEmail: email, submittedPassword: password })

            axios.put('https://office-essentials-app.herokuapp.com/office-essentials/User/login/', {
                user_email: email,
                user_password: password
            },{
                headers: {
                    // 'application/json' is the modern content-type for JSON, but some
                    // older servers may use 'text/json'.
                    // See: http://bit.ly/text-json
                    'content-type': 'application/json'
                }})
                .then(response => {
                    if(response.data === null) {
                        alert("User or password incorrect, try again.")
                    }
                    else {
                        storeData.set('id', response.data[0].toString())
                        window.location = "/UserView";
                        //console.log(storeData.get('id'))
                    }

                }, error => {
                    console.log(error)
                });
        }
    }

    handleNewUserSubmit = () => {
        const { emailNew, passwordNew, firstName, lastName, phoneNum } = this.state

        if (emailNew === '' || passwordNew === '' || firstName === '' || lastName === '' || phoneNum === ''){
            alert('Please enter the complete data.')
        }

        else {

            this.setState({ submittedEmail: emailNew, submittedPassword: passwordNew, submittedFirstName: firstName, submittedLastName: lastName, submittedPhoneNum: phoneNum })

            axios.post('https://office-essentials-app.herokuapp.com/office-essentials/User/all',{
                user_email: emailNew,
                user_password: passwordNew,
                user_firstname: firstName,
                user_lastname: lastName,
                user_phone: phoneNum,
                user_type: 'regular'
            }, {
                headers: {
                    // 'application/json' is the modern content-type for JSON, but some
                    // older servers may use 'text/json'.
                    // See: http://bit.ly/text-json
                    'content-type': 'application/json'
                }})
                .then(response => {
                    if(response.data === 0){
                        alert("Email already in use, please try another.")
                    } else {
                        storeData.set('id', response.data[0]['user_id'])
                        window.location = "/UserView";
                        //console.log(storeData.get('id'))
                    }
                }, error => {
                    console.log(error)
                });


        }
    }
    render() {

        const { email, password, emailNew, passwordNew, firstName, lastName, phoneNum, submittedEmail, submittedPassword,submittedFirstName, submittedLastName, submittedPhoneNum } = this.state

        return (

            <div>
                <Header className='home-header'>Office Essential's DB Demo</Header>
                <Header className='home-sub'as='h5'>Please Log in with existing credentials or Register.</Header>
                <Segment className='home-segment' raised>
                    <Grid columns={2} relaxed='very' stackable grid>
                        <Grid.Column verticalAlign='middle'>
                            <Form onSubmit={this.handleUserSubmit}>
                                <Form.Input nameClass='form-input' required
                                    icon='user'
                                    iconPosition='left'
                                    placeholder='Email'
                                    name='email'
                                    value={email}
                                    onChange={this.handleUserChange}
                                    label='Email'
                                    labelPosition='left'
                                    labelcolor=''
                                    style={{ color: "rgba(54, 65, 80, 1)"}}
                                />
                                <Form.Input nameClass='form-input' required
                                    icon='lock'
                                    iconPosition='left'
                                    placeholder='Password'
                                    name='password'
                                    value={password}
                                    type='password'
                                    onChange={this.handleUserChange}
                                    label='Password'
                                            style={{ color: "rgba(54, 65, 80, 1)"}}

                                />
                                <Form.Button id='form-button' content='Log in' size ='medium'  />

                            </Form>
                        </Grid.Column>
                        <Grid.Column verticalAlign='middle'>
                            <Form nameClass='form' onSubmit={this.handleNewUserSubmit}>
                                <Form.Input nameClass='form-input'required
                                    icon='user'
                                    iconPosition='left'
                                    placeholder='Email'
                                    name='emailNew'
                                    value={emailNew}
                                    onChange={this.handleNewUserChange}
                                    label='Email'
                                            style={{ color: "rgba(54, 65, 80, 1)"}}
                                />

                                <Form.Input nameClass='form-input' required
                                    icon='lock'
                                    iconPosition='left'
                                    placeholder='Password'
                                    name='passwordNew'
                                    value={passwordNew}
                                    type='password'
                                    onChange={this.handleNewUserChange}
                                    label='Password'
                                            style={{ color: "rgba(54, 65, 80, 1)"}}
                                />

                                <Form.Input nameClass='form-input' required
                                    icon='address book'
                                    iconPosition='left'
                                    name='firstName'
                                    value={firstName}
                                    onChange={this.handleNewUserChange}
                                    placeholder='First Name'
                                    label='First Name'
                                            style={{ color: "rgba(54, 65, 80, 1)"}}
                                />

                                <Form.Input nameClass='form-input' required
                                    icon='address book'
                                    iconPosition='left'
                                    name='lastName'
                                    value={lastName}
                                    onChange={this.handleNewUserChange}
                                    placeholder='Last Name'
                                    label='Last Name'
                                            style={{ color: "rgba(54, 65, 80, 1)"}}
                                    />

                                <Form.Input required
                                    icon='phone'
                                    iconPosition='left'
                                    name='phoneNum'
                                    value={phoneNum}
                                    onChange={this.handleNewUserChange}
                                    placeholder='Phone'
                                    label='Phone'
                                    style={{ color: "rgba(54, 65, 80, 1)"}}/>

                                <Form.Button id='form-button' content='Sign up' icon='signup' size='medium' />

                            </Form>
                        </Grid.Column>
                    </Grid>
                    <Divider vertical style={{ color: "rgba(245, 244, 243, 1)" }} >Or</Divider>
                </Segment>

            </div>


        )
    }

}


export default CheckingAuth;