import React, {useState, useEffect} from 'react'
import { Button, Header, Icon, Modal } from 'semantic-ui-react'
import CheckOutProducts from "./CheckOutProducts";
import * as storeData from "store";
import "./Checkout.css"
import axios from "axios";

function CheckOut() {
    const [open, setOpen] = React.useState(false);
    const [subtotal, setSubtotal] = useState(0);
    let tax = Math.round(((subtotal*0.115) + Number.EPSILON) * 100) / 100;
    let total = Math.round((tax + subtotal + Number.EPSILON) * 100) / 100;

    function handleCheckOut() {
        console.log('entered')
        axios.post('https://office-essentials-app.herokuapp.com/office-essentials/Orders/neworder', {
            user_id: storeData.get('id'),
        })
            .then(response => {
                console.log(response)
                if (response.status === 201){
                    alert('Order has been completed!')
                    setOpen(false)
                    window.location.reload()
                } else {
                    alert(response.data[0])
                    setOpen(false)
                    window.location.reload()
                }
            },  error => {
                alert(error.response.data)
                setOpen(false)
                window.location.reload()
            })
    }

    function handleSubtotal(){
        axios.get('https://office-essentials-app.herokuapp.com/office-essentials/CartContents/getsubtotal/' + storeData.get('cartID'))
            .then(response => {
                console.log(response)
                setSubtotal(Math.round(((response.data[0][0]) + Number.EPSILON) * 100) / 100);
            },  error => {
                console.log('getting there')
                console.log(error)
            })
    }

    return (
        <Modal
            closeIcon
            open={open}
            trigger={<Button onClick={() => handleSubtotal()}>Check Out</Button>}
            onClose={() => setOpen(false)}
            onOpen={() => setOpen(true)}
        >
            <Header icon='box' content='Checkout' />
            <Modal.Content>
                <CheckOutProducts />
                <h3 className="checkout-heading-style">Subtotal: {subtotal}</h3>
                <h3 className="checkout-heading-style">Tax: {tax} </h3>
                <h3 className="checkout-heading-style">Total: {total}</h3>
            </Modal.Content>
            <Modal.Actions>
                <Button color='red' onClick={() => setOpen(false)}>
                    <Icon name='remove' /> Cancel
                </Button>
                <Button color='green' onClick={() => handleCheckOut()}>
                    <Icon name='checkmark' /> Confirm Order
                </Button>
            </Modal.Actions>
        </Modal>
    )
}

export default CheckOut;