import {Button, Card} from "semantic-ui-react";
import React, {useState, useEffect} from "react";
import OrderDetails from "./OrderDetails";
import "./Order.css";
import axios from "axios";
import * as storeData from "store";

function OrderCard() {

    const [data, setData] = useState([]);

    // Setting initial data to what is currently in the cart
    // had to change method to post because axios ignores bodies within get methods
    useEffect(() => {
        const fetchItems = async () => {
            try {
                const response = await axios.post('https://office-essentials-app.herokuapp.com/office-essentials/Orders/orderhistory2',
                    {"user_id":storeData.get('id')}
                );
                console.log(response.data)
                setData(response.data)
            } catch(err) {
                if (err.response) {
                    alert(err.response.data)
                    console.log(err.response.data);
                    console.log(err.response.status);
                    console.log(err.response.headers);
                    window.location.reload()
                }
                else{
                    console.log(`Error: ${err.message}`);
                }
            }
        }
        fetchItems();
    }, [data]);

    return data.map(value => {return <Card key={value.OrderID}>
        <Card.Content>
            <Card.Header>Order # {value.OrderID}</Card.Header>
            <Card.Description>
                Order Placed: {value.OrderDate} <br/>
                Subtotal: {value.OrderSubtotal} <br/>
                Tax: {value.OrderTax}<br/>
                Total: {value.OrderTotal}
            </Card.Description>
        </Card.Content>
        <Card.Content extra>
            <div className="modal-style">
                <OrderDetails info={value.Items} />
            </div>
        </Card.Content>
    </Card>
    });
}

export default OrderCard;
