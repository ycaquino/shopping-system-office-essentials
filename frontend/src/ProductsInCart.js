import React, { useState, useEffect} from 'react';
import {Button, Card} from "semantic-ui-react";
import axios from "axios";
import "./ProductsInCart.css"
import * as storeData from "store";

function ProductsInCart() {
    const [data, setData] = useState([]);
    // const [quantityToBeRemoved, setQuantityToBeRemoved] = useState(1)

    // Setting initial data to what is currently in the cart
    useEffect(() => {
        const fetchItems = async () => {
            try {
                const response = await axios.get('https://office-essentials-app.herokuapp.com/office-essentials/CartContents/getallfromcart/' + storeData.get('cartID'));
                setData(response.data);
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

    // updating data once an element is deleted
    const handleDelete = async (event) => {
        event.preventDefault();
        console.log(event.target.product_id.value);
        console.log(event.target.cart_id.value);
        try {
            const quantityToBeRemoved = event.target.quantity_to_be_removed.value;
            const cartID = event.target.cart_id.value;
            const productID = event.target.product_id.value;
            const response = await axios.delete('https://office-essentials-app.herokuapp.com/office-essentials/CartContents', {
                data:{"CartId":Number(cartID),
                    "ProductId":Number(productID),
                    "ProductQuantity":Number(quantityToBeRemoved)
                }
            });
            setData(response.data);
        } catch (err) {
            console.log(`Error: ${err.message}`);
        }
    }

    // const quantityToBeRemovedHandler = (event) => {
    // }
    //
    // const plusEventHandler = (event) => {
    //     console.log(event.target)
    //     setQuantityToBeRemoved(prevState => prevState + 1)
    // }
    //
    // const minusEventHandler = (event) => {
    //     setQuantityToBeRemoved(prevState => prevState - 1)
    // }

    return data.map(value => {return <Card key={value.ProductId}>
        <Card.Content>
            <Card.Header>{value.ProductName}</Card.Header>
            <Card.Meta>Price: ${value.ProductPrice}</Card.Meta>
            {/*<Card.Description>Discount: {value.discount * 100}%</Card.Description>*/}
            <Card.Description>
                Quantity: {value.ProductQuantity}
            </Card.Description>
        </Card.Content>
        <Card.Content extra>
            <form onSubmit={handleDelete}>
                <div>
                    <label htmlFor="quantity_to_be_removed">Quantity to be removed: </label>
                    {/*<button onClick={minusEventHandler}>Minus</button>*/}
                    <input name="quantity_to_be_removed" type="number" min="1"
                           max={value.ProductQuantity} defaultValue="1"/>
                    {/*<button onClick={plusEventHandler}>plus</button>*/}
                    <label htmlFor="cart_id" />
                    <input name="cart_id" type="hidden" value={value.CartId}/>
                    <label htmlFor="product_id"/>
                    <input name="product_id" type="hidden" value={value.ProductId}/>
                </div>
                <div className="delete-button">
                    <Button type="submit" basic color='red'>
                        Remove From Cart
                    </Button>
                </div>
            </form>
        </Card.Content>
    </Card>});

}

export default ProductsInCart;
