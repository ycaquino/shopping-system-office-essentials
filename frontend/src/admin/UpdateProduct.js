import React, {Component, useState} from 'react'
import {Form, Header} from 'semantic-ui-react'
import axios from "axios";
import * as storeData from "store";

function UpdateProduct(){
    const [id, setId] = useState('');
    const [name, setName] = useState('');
    const [price, setPrice] = useState('');
    const [discount, setDiscount] = useState('');
    const [category, setCategory] = useState('');
    const [quantity, setQuantity] = useState('');

    const handleChange = (e) => {

        if(e.target.name === 'id'){
            setId(e.target.value);
        }
        if(e.target.name === 'name'){
            setName(e.target.value);
        }
        if(e.target.name === 'price'){
            setPrice(e.target.value);
        }
        if(e.target.name === 'discount'){
            setDiscount(e.target.value);
        }
        if(e.target.name === 'category'){
            setCategory(e.target.value);
        }
        if(e.target.name === 'quantity'){
            setQuantity(e.target.value);
        }
    }

    const handleSubmit = (e) => {
        e.preventDefault();
        const data = {
            product_id: id,
            product_name: name,
            product_price: price,
            product_dis: discount,
            product_quantity: quantity,
            product_category: category,
            active: true,
            user_id: storeData.get('id')
        }
        axios.post('https://office-essentials-app.herokuapp.com/office-essentials/products/id/'+id, data, {headers:{'content-type': 'application/json'}})
            .then(res => {
                alert('Product Updated Successfully')
                console.log(res)
            })
            .catch(err => {
                alert('Error Updating Product')
                console.log(category)
                console.log(storeData.get('id'))
                console.log(err)
            });
        setId('');
        setName('');
        setPrice('');
        setDiscount('');
        setCategory('');
        setQuantity('');
    };

    return (
        <div>
            <Header as='h2' textAlign='center'>Update Product</Header>
            <Form onSubmit={handleSubmit}>
                <Form.Field>
                    <label>Product ID</label>
                    <input placeholder='Product ID' name='id' value={id} onChange={handleChange}/>
                </Form.Field>
                <Form.Field>
                    <label>Product Name</label>
                    <input placeholder='Product Name' name='name' value={name} onChange={handleChange}/>
                </Form.Field>
                <Form.Field>
                    <label>Product Price</label>
                    <input placeholder='Product Price' name='price' value={price} onChange={handleChange}/>
                </Form.Field>
                <Form.Field>
                    <label>Product Discount</label>
                    <input placeholder='Product Discount' name='discount' value={discount} onChange={handleChange}/>
                </Form.Field>
                <Form.Field>
                    <label>Product Category</label>
                    <input placeholder='Product Category' name='category' value={category} onChange={handleChange}/>
                </Form.Field>
                <Form.Field>
                    <label>Product Quantity</label>
                    <input placeholder='Product Quantity' name='quantity' value={quantity} onChange={handleChange}/>
                </Form.Field>
                <Form.Button content='Submit'/>
            </Form>
        </div>
    )
}
export default UpdateProduct;