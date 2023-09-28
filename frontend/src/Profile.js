import React, {Component, useEffect, useState} from 'react';
import * as storeData from "store";
import axios from "axios";
import {Container, Segment} from "semantic-ui-react";

function Profile() {

    const id = storeData.get('id')

    const [userData, setUserData] = useState([])

    useEffect(() => {
        axios.put('https://office-essentials-app.herokuapp.com/office-essentials/User/id/', {
            user_id: id
        })
            .then((response =>
                    setUserData(response.data)
            ))
    }, [])


    return (<Container>
            <Segment className='profile'>
                <p><b>Email:</b> {userData.user_email}
                </p>
                <p><b>First Name:</b> {userData.user_firstname}</p>
                <p><b>Last Name:</b> {userData.user_lastname}</p>
                <p><b>Phone Number:</b> {userData.user_phone}</p>
            </Segment>
        </Container>
    )

}

export default Profile;