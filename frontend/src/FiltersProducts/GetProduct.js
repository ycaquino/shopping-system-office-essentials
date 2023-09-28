import React, {Component, useEffect, useState} from 'react';
import {Card, Form, Grid, Header} from "semantic-ui-react";
import axios from "axios";
import AllProducts from "../AllProducts";
import * as storeData from "store";

function GetProduct(){
    const [product, setProduct] = useState({});
    const [productId, setProductId] = useState(0);
    const [wishlistID, setWishlistID] = useState(0)
    const [cartID, setCartID] = useState(0)
    const id = storeData.get('id');

    const handleChange = (event) => {
        setProductId(event.target.value);
    };

    const handleSubmit = (event) => {
        event.preventDefault();
        axios.get('https://office-essentials-app.herokuapp.com/office-essentials/products/id/' + productId)
            .then(response => {
                setProduct(response.data);
            })
            .catch(error => {
                alert("Product not found!");
                console.log(error);
            });
    };


    let products_info = [];


        products_info.push({
            "id": product.product_id,
            "name": product.product_name,
            "price": product.product_price,
            "discount": product.product_dis,
            "category": product.product_category,
            "quantity": product.product_quantity
        });

    useEffect(() => {
        axios.get('https://office-essentials-app.herokuapp.com/office-essentials/Wishlist/' + id)
            .then(response => {
                setWishlistID(response.data[0][0])

            }, error => {
                console.log(error);
            });

        axios.get('https://office-essentials-app.herokuapp.com/office-essentials/Cart/' + id)
            .then(response => {
                setCartID(response.data[0])
            }, error => {
                console.log(error)
            })
    }, [])

    return (
        console.log(products_info),
        <Grid>
            <Grid.Row centered>
            <Form onSubmit={handleSubmit}>
                <Form.Field >
                    <label>Search Product ID</label>
                    <input placeholder='Product ID' onChange={handleChange}/>
                </Form.Field>
                <Form.Button>Submit</Form.Button>
            </Form>
            <Card.Group raised>
                <AllProducts info={products_info} wishlistid = {wishlistID} cartid={cartID}/>
            </Card.Group>
            </Grid.Row>
        </Grid>
    );
}
export default GetProduct;