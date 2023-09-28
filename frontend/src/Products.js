import React, {Component, useEffect, useState} from 'react';
import {Button, Card, Container, Modal, Tab} from "semantic-ui-react";
import axios from "axios";
import AllProducts from "./AllProducts";
import * as storeData from "store";


function Products() {

    const [productData, setProductData] = useState([]);

    const retrieveProducts = async () => {
        const response = await axios.get('https://office-essentials-app.herokuapp.com/office-essentials/products/all');
        return response.data;
    }

    useEffect(() => {
        const getAllProducts = async () => {
            const allProducts = await retrieveProducts();
            if(allProducts) {
                setProductData(allProducts);
            }
        }
        getAllProducts();
    } , []);

    let products_info = [];

    for(let i = 0; i < productData.length; i++) {
        products_info.push({
            "id": productData[i].product_id,
            "name": productData[i].product_name,
            "price": productData[i].product_price,
            "discount": productData[i].product_dis,
            "category": productData[i].product_category,
            "quantity": productData[i].product_quantity
        });
    }

    const id = storeData.get('id');

    const [wishlistID, setWishlistID] = useState(0)
    const [cartID, setCartID] = useState(0)


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


    return <Card.Group raised>
        <AllProducts info={products_info} wishlistid = {wishlistID} cartid={cartID}/>
    </Card.Group>
}

export default Products;
