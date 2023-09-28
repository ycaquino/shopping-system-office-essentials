import {Card} from "semantic-ui-react";
import React from "react";

function OrderContents(props) {

    return props.info.map(value => <Card fluid>
        <Card.Content>
            <Card.Header>{value.ProductName}</Card.Header>
            <Card.Description>
                Quantity: {value.ProductQuantity} <br/>
                Price: {value.ProductPrice}<br/>
            </Card.Description>
        </Card.Content>
    </Card>);
}

export default OrderContents;
