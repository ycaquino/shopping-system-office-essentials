import React, {Component, useState} from 'react';
import {Button, Card, Container, Modal, Tab} from "semantic-ui-react";
import axios from "axios";
import "./AllProducts.css"

function AllProducts(props) {
    console.log(props.wishlistid)
    const [quantityToBeAdded, setQuantityToBeAdded] = useState(1)

    function addProductWishlist (product_id, wishlist_id) {
        const addition = 'https://office-essentials-app.herokuapp.com/office-essentials/Wishlist/' + wishlist_id + '/' + product_id
        // console.log(addition)
        axios.get(addition)
            .then(r =>
                alert("Product added!")
            )
    }

    function addProductCart(product_id, cart_id){
        axios.post('https://office-essentials-app.herokuapp.com/office-essentials/CartContents', {
            CartId: cart_id,
            ProductId: product_id,
            ProductQuantity: Number(quantityToBeAdded)
        })
            .then(response => {
                alert('Product added to cart!')
            },  error => {
                alert(error.response.data)
                console.log(error)
            })
    }

    function updateQuantity(event){
        // console.log(event.target.value)
        setQuantityToBeAdded(event.target.value)
    }


    //props.info.forEach(value => console.log(value.pname));
    return props.info.map(value => {return <Card>
        <Card.Content>

            <Card.Header>{value.name}</Card.Header>
            <Card.Meta>Price: ${value.price}</Card.Meta>
            <Card.Description>Discount: {value.discount * 100}%</Card.Description>
            <Card.Description>Quantity: {value.quantity}</Card.Description>
            <Card.Description>
                {value.category}
            </Card.Description>
        </Card.Content>
        <Card.Content extra>
            <div>
                <label htmlFor="quantity-to-be-added">Quantity to be added: </label>
                <input type="number" onChange={(event) => updateQuantity(event)}
                       name="quantity-to-be-added" min="1" max={value.quantity} defaultValue="1" />
            </div>
            <div className='ui two buttons btn-style'>
                <Button  className='active-button' onClick={() => addProductWishlist(value.id, props.wishlistid)}>
                    Add to Wish List
                </Button>
                {value.quantity === 0 ?
                    (<Button className='non-active-button'>Not in stock</Button>) :
                    (<Button className='active-button' onClick={() => addProductCart(value.id, props.cartid)}>
                    Add to Cart
                </Button>)}

            </div>
        </Card.Content>
    </Card>});
}
export default AllProducts;
