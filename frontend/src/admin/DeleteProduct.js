import React, {Component, useState, useEffect} from 'react'
import {Form, Header} from 'semantic-ui-react'
import axios from "axios";
import * as storeData from "store";

function DeleteProduct(){
    const [product, setProduct] = useState('');

    const handleChange = (e) => {
        setProduct(e.target.value);
    }



    const handleSubmit = (e) => {
        e.preventDefault()
        axios.delete(`https://office-essentials-app.herokuapp.com/office-essentials/products/id/` + product + '/user/' + storeData.get('id'))
            .then(response => {
                alert("Product deleted successfully")
                console.log(response)
                console.log(product)
                console.log(storeData.get('id'))
            })
            .catch(err => {
                alert("Product not deleted")
                console.log(product)
                console.log(storeData.get('id'))
                console.log(err.response)
            })
    }

    return(
        <div>
            <Header as='h2' textAlign='center'>Delete Product</Header>
            <Form onSubmit={handleSubmit}>
                <Form.Field>
                    <label>Product ID</label>
                    <input placeholder='Product ID' onChange={handleChange}/>
                </Form.Field>
                <Form.Button content='Delete'/>
            </Form>

        </div>
    )
}

export default DeleteProduct