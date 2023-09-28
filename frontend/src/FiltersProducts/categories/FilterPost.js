import React, {Component, useEffect, useState} from 'react';
import {Button, Card, Container, Modal, Tab} from "semantic-ui-react";
import axios from "axios";
import AllProducts from "../../AllProducts";

function FilterPost(props) {
    const [categoryData, setCategoryData] = useState([]);


    const retrieveCategory = async () => {
        const response = await axios.get('https://office-essentials-app.herokuapp.com/office-essentials/products/category/Post-It & Sticky Notes');
        return response.data;
    }

    useEffect(() => {
        const getCategory = async () => {
            const allProducts = await retrieveCategory();
            if(allProducts) {
                setCategoryData(allProducts);
            }
        }
        getCategory();
    } , []);

    let categories_info = [];

    for(let i = 0; i < categoryData.length; i++) {
        categories_info.push({
            "id": categoryData[i].product_id,
            "name": categoryData[i].product_name,
            "price": categoryData[i].product_price,
            "discount": categoryData[i].product_dis,
            "category": categoryData[i].product_category,
            "quantity": categoryData[i].product_quantity
        });
    }

    return <Card.Group>
        <AllProducts info={categories_info}/>
    </Card.Group>

}

export default FilterPost;