import React, {useState, useEffect} from 'react'
import { Button, Header, Icon, Modal } from 'semantic-ui-react'
import OrderContents from './OrderContents'
import axios from "axios";

function OrderDetails(props) {
    const [open, setOpen] = React.useState(false);

    return (
        <Modal
            closeIcon
            open={open}
            trigger={<Button>Order Details</Button>}
            onClose={() => setOpen(false)}
            onOpen={() => setOpen(true)}
        >
            <Header icon='box' content='Order Details' />
            <Modal.Content>
                <OrderContents info={props.info}/>
            </Modal.Content>
            <Modal.Actions>
                <Button color='green' onClick={() => setOpen(false)}>
                    <Icon name='check' /> Done
                </Button>
            </Modal.Actions>
        </Modal>
    )
}

export default OrderDetails;