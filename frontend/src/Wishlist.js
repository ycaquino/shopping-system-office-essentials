import React, {Component, useEffect, useState} from 'react';
import {Button, Card, CardGroup, Container, Modal, Tab} from "semantic-ui-react";
import * as storeData from "store";
import axios from "axios";






function AllProductsInWishlist(props) {
    function deleteProduct (product_id, wishlist_id) {
        const addition = 'https://office-essentials-app.herokuapp.com/office-essentials/Wishlist/' + wishlist_id + '/' + product_id
        // console.log(addition)
        axios.delete(addition)
            .then(r =>
                alert("Product deleted")
            )
    }

    function addToCart(cart_id, product_id) {
        axios.post('https://office-essentials-app.herokuapp.com/office-essentials/CartContents', {
            CartId: cart_id,
            ProductId: product_id,
            ProductQuantity: 1
        })
            .then(response => {
                alert('Product added to cart!')
            },  error => {
                console.log(error)
            })
    }

    // props.info.forEach(value => console.log(value.pname));
    return props.info.map(value => {return <Card key={value[0]}>
        <Card.Content>
            <Card.Header>{value[1]}</Card.Header>
            <Card.Meta><b>Price </b>: ${value[2]}</Card.Meta>
            <Card.Description>Discount: {value[3] * 100}%</Card.Description>
            <Card.Description>
                {value[4]===0 ? (
                    <p>Product no longer available. Check later for updates</p>
                ): (<p>Quantity: {value[4]}</p>)}
            </Card.Description>
        </Card.Content>
        <Card.Content extra>
            <div className='ui two buttons'>

                <Button className='active-button delete' onClick={() => deleteProduct(value[0], props.wishlistid)}>
                    Delete from Wishlist
                </Button>
                {value[4]===0 ? (
                    <Button className='non-active-button' >
                        Not in Stock
                    </Button>
                ):(<Button className='active-button' onClick={() => addToCart(props.cartid, value[0])}>
                    Add to Cart
                </Button>
                )}

            </div>
        </Card.Content>
    </Card>});
}

function Wishlist() {
    const id = storeData.get('id');
    const [wishlistID, setWishlistID] = useState(0)
    const [products, setProducts] = useState([])
    const [cartID, setCartID] = useState(0)

    axios.get('https://office-essentials-app.herokuapp.com/office-essentials/Wishlist/' + id)
        .then(response =>{
            setWishlistID(response.data[0][0])
            setProducts(response.data.slice(1))

        }, error => {
            console.log(error);
        });

    useEffect(() => {
        axios.get('https://office-essentials-app.herokuapp.com/office-essentials/Cart/' + id)
            .then(response => {
                setCartID(response.data[0])
            }, error => {
                console.log(error)
            })
    }, [])



    return (<CardGroup>
        <AllProductsInWishlist info={products} wishlistid = {wishlistID} cartid={cartID}/>
    </CardGroup>)


}

export default Wishlist;
