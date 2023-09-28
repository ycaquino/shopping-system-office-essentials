import React, { useState, useEffect} from 'react';
import {Card} from "semantic-ui-react";
import * as storeData from "store";
import axios from "axios";
import "./ProductsInCart.css"

function ProductsInCart() {
    const [data, setData] = useState([]);
    let subtotal = 0;

    // Setting initial data to what is currently in the oder
    useEffect(() => {
        const fetchItems = async () => {
            try {
                const response = await axios.get('https://office-essentials-app.herokuapp.com/office-essentials/CartContents/getallfromcart/' + storeData.get('cartID'));
                setData(response.data);
            } catch(err) {
                if (err.response) {
                    console.log(err.response.data);
                    console.log(err.response.status);
                    console.log(err.response.headers);
                }
                else{
                    console.log(`Error: ${err.message}`);
                }
            }
        }
        fetchItems();
    }, []);

    // axios.get('http://127.0.0.1:5000/office-essentials/CartContents/getallfromcart/18')
    //     .then(response => setData(response.data))

    return data.map(value => {return <Card fluid key={value.ProductId}>
        <Card.Content>
            <Card.Header>{value.ProductName}</Card.Header>
            <Card.Description>
                Price: {value.ProductPrice}<br></br>
                Quantity: {value.ProductQuantity}
            </Card.Description>
        </Card.Content>
    </Card>});

}

export default ProductsInCart;