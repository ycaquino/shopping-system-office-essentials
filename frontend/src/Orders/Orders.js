import React from 'react';
import {Card} from "semantic-ui-react";
import OrderCard from "./OrderCard"

function Cart() {
    return (
            <Card.Group>
                <OrderCard />
            </Card.Group>
    )
}

export default Cart;