import React from 'react';
import {Card} from "semantic-ui-react";
import ProductsInCart from "./ProductsInCart";
import CheckOut from "./checkOut";
import "./Cart.css"

function Cart() {
    return (  <div>
            <Card.Group>
                <ProductsInCart />
            </Card.Group>
            <div className="checkout-button">
                <CheckOut />
            </div>
    </div>
    )
}

export default Cart;