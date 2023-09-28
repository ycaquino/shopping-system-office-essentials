import React, {Component, useEffect, useState} from 'react';
import {Button, Card, Container, Modal, Tab} from "semantic-ui-react";
import axios from "axios";
import AllProducts from "../AllProducts";

function FilterPriceDesc(prop) {
    const [orderData, setOrderData] = useState([]);

    const retrieveOrder = async () => {
        const response = await axios.get('https://office-essentials-app.herokuapp.com/office-essentials/products/price/desc');
        return response.data;
    };

    useEffect(() => {
        const getOrder = async () => {
            const allProducts = await retrieveOrder();
            if(allProducts) {
                setOrderData(allProducts);
            }
        }
        getOrder();
    } , []);

    let order_info = [];

    for(let i = 0; i < orderData.length; i++) {
        order_info.push({
            "id": orderData[i].product_id,
            "name": orderData[i].product_name,
            "price": orderData[i].product_price,
            "discount": orderData[i].product_dis,
            "category": orderData[i].product_category,
            "quantity": orderData[i].product_quantity
        });
    }

    return <Card.Group>
        <AllProducts info={order_info}/>
    </Card.Group>

}

export default FilterPriceDesc;