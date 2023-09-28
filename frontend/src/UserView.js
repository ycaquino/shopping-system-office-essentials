import React, {Component, useCallback, useState} from 'react';
import {
    Button,
    Card,
    Container,
    Divider,
    Grid,
    GridColumn,
    Header,
    Icon,
    Modal,
    Segment,
    Tab,
    Menu,
    Dropdown,
    Form
} from "semantic-ui-react";
import Dashboard from "./Dashboard";
import Products from "./Products";
import Cart from "./Cart";
import Orders from "./Orders/Orders";

import FilterPriceAsc from "./FiltersProducts/FilterPriceAsc";
import FilterPriceDesc from "./FiltersProducts/FilterPriceDesc";
import FilterNameDesc from "./FiltersProducts/FilterNameDesc";
import FilterNameAsc from "./FiltersProducts/FilterNameAsc";
import FilterBinders from "./FiltersProducts/categories/FilterBinders";
import FilterPaper from "./FiltersProducts/categories/FilterPaper";
import FilterDeskOrg from "./FiltersProducts/categories/FilterDeskOrg";
import FilterEnvelopes from "./FiltersProducts/categories/FilterEnvelopes";
import FilterNotebooks from "./FiltersProducts/categories/FilterNotebooks";
import FilterPens from "./FiltersProducts/categories/FilterPens";
import FilterPost from "./FiltersProducts/categories/FilterPost";
import FilterScissors from "./FiltersProducts/categories/FilterScissors";
import FilterStaplers from "./FiltersProducts/categories/FilterStaplers";
import FilterStickers from "./FiltersProducts/categories/FilterStickers";
import DeleteProduct from "./admin/DeleteProduct";
import CreateProduct from "./admin/CreateProduct";
import UpdateProduct from "./admin/UpdateProduct";
import GetProduct from "./FiltersProducts/GetProduct";
import Wishlist from "./Wishlist"
import * as storeData from "store";
import Profile from "./Profile";
import axios from "axios";
import './UserView.css'




function CheckingAuth() {
    if(typeof storeData.get('id') === 'undefined'){
        return (<Container align='center'>
            <Header>Access denied.</Header>
            <Divider />
            <Button content="Click here to be redirected to Log-In" onClick={(event => {window.location = '/Home'})}/>
        </Container>)
    }

    else {
        return <UserView />
    }

}

function UserView(props){
    // console.log(storeData.get('id'))
    let handleLogOut = () => {
        storeData.remove('id')
        storeData.remove('cartID')
        window.location = '/Home'
    }

    const [userType, setUserType] = useState("")

    let addition = 'https://office-essentials-app.herokuapp.com/office-essentials/User/Type/' + storeData.get('id')

    axios.get(addition)
        .then(response => {
            setUserType(response.data[0])
        }, error => {
            console.log(error)
        })

    axios.get('https://office-essentials-app.herokuapp.com/office-essentials/Cart/' + storeData.get('id'))
        .then(response => {
            console.log(response.data[0])
            storeData.set('cartID', response.data[0])
        }, error => {
            console.log(error)
        })

    const [active, setActive] = useState(<Products/>)
    const [adminActive, setAdminActive] = useState(<CreateProduct/>)
    const [isAuth, setIsAuth] = useState(true)
    const [notShow, setNotShow] = useState(false)
    const [open, setOpen] = useState(false)
    const panes = [
        {
            menuItem: 'Products', render: () => <Tab.Pane active={isAuth}>
                <Container>
                    <Menu>
                        <Dropdown text='Categories' pointing className='link item'>
                            <Dropdown.Menu>
                                <Dropdown.Item onClick={() => setActive(<Products/>)}>All</Dropdown.Item>
                                <Dropdown.Item onClick={() => setActive(<FilterPost/>)}>Post-It & Sticky Notes</Dropdown.Item>
                                <Dropdown.Item onClick={() => setActive(<FilterStaplers/>)}>Staplers & Staples</Dropdown.Item>
                                <Dropdown.Item onClick={() => setActive(<FilterPens/>)}>Pens, Pencils & Markers</Dropdown.Item>
                                <Dropdown.Item onClick={() => setActive(<FilterPaper/>)}>Paper & Binder Clips</Dropdown.Item>
                                <Dropdown.Item onClick={() => setActive(<FilterScissors/>)}>Scissors</Dropdown.Item>
                                <Dropdown.Item onClick={() => setActive(<FilterEnvelopes/>)}>Envelopes</Dropdown.Item>
                                <Dropdown.Item onClick={() => setActive(<FilterNotebooks/>)}>Notebooks & Journals</Dropdown.Item>
                                <Dropdown.Item onClick={() => setActive(<FilterBinders/>)}>Binders</Dropdown.Item>
                                <Dropdown.Item onClick={() => setActive(<FilterDeskOrg/>)}>Desk Organizer</Dropdown.Item>
                                <Dropdown.Item onClick={() => setActive(<FilterStickers/>)}>Stickers</Dropdown.Item>
                            </Dropdown.Menu>
                        </Dropdown>
                        <Dropdown text='Price Sort' pointing className='link item'>
                            <Dropdown.Menu>
                                <Dropdown.Item onClick={() => setActive(<FilterPriceAsc/>)}>Lowest to Highest</Dropdown.Item>
                                <Dropdown.Item onClick={() => setActive(<FilterPriceDesc/>)}>Highest to Lowest</Dropdown.Item>
                            </Dropdown.Menu>
                        </Dropdown>
                        <Dropdown text='Name Sort' pointing className='link item'>
                            <Dropdown.Menu>
                                <Dropdown.Item onClick={() => setActive(<FilterNameAsc/>)}>A...Z</Dropdown.Item>
                                <Dropdown.Item onClick={() => setActive(<FilterNameDesc order = 'desc'/>)}>Z...A</Dropdown.Item>
                            </Dropdown.Menu>
                        </Dropdown>
                    </Menu>
                </Container>
                {active}
            </Tab.Pane>
        },
        {
            menuItem: 'WishList', render: () => <Tab.Pane active={isAuth}><Wishlist /></Tab.Pane>
        },
        {
            menuItem: 'Cart', render: () => <Tab.Pane active={isAuth}><Cart/></Tab.Pane>
        },
        {
            menuItem: 'Profile', render: () => <Tab.Pane active={isAuth}><Profile /></Tab.Pane>
        },
        {
            menuItem: 'Dashboard', render: () => <Tab.Pane active={isAuth}><Dashboard/></Tab.Pane>
        },
        {
            menuItem: 'My Orders', render: () => <Tab.Pane active={isAuth}><Orders/></Tab.Pane>
        }
    ]

    const userPanes = [
        {
            menuItem: 'Products', render: () => <Tab.Pane active={isAuth}>
                <Container>
                    <Menu>
                        <Dropdown text='Categories' pointing className='link item'>
                            <Dropdown.Menu>
                                <Dropdown.Item onClick={() => setActive(<Products/>)}>All</Dropdown.Item>
                                <Dropdown.Item onClick={() => setActive(<FilterPost/>)}>Post-It & Sticky Notes</Dropdown.Item>
                                <Dropdown.Item onClick={() => setActive(<FilterStaplers/>)}>Staplers & Staples</Dropdown.Item>
                                <Dropdown.Item onClick={() => setActive(<FilterPens/>)}>Pens, Pencils & Markers</Dropdown.Item>
                                <Dropdown.Item onClick={() => setActive(<FilterPaper/>)}>Paper & Binder Clips</Dropdown.Item>
                                <Dropdown.Item onClick={() => setActive(<FilterScissors/>)}>Scissors</Dropdown.Item>
                                <Dropdown.Item onClick={() => setActive(<FilterEnvelopes/>)}>Envelopes</Dropdown.Item>
                                <Dropdown.Item onClick={() => setActive(<FilterNotebooks/>)}>Notebooks & Journals</Dropdown.Item>
                                <Dropdown.Item onClick={() => setActive(<FilterBinders/>)}>Binders</Dropdown.Item>
                                <Dropdown.Item onClick={() => setActive(<FilterDeskOrg/>)}>Desk Organizer</Dropdown.Item>
                                <Dropdown.Item onClick={() => setActive(<FilterStickers/>)}>Stickers</Dropdown.Item>
                            </Dropdown.Menu>
                        </Dropdown>
                        <Dropdown text='Price Sort' pointing className='link item'>
                            <Dropdown.Menu>
                                <Dropdown.Item onClick={() => setActive(<FilterPriceAsc/>)}>Lowest to Highest</Dropdown.Item>
                                <Dropdown.Item onClick={() => setActive(<FilterPriceDesc/>)}>Highest to Lowest</Dropdown.Item>
                            </Dropdown.Menu>
                        </Dropdown>
                        <Dropdown text='Name Sort' pointing className='link item'>
                            <Dropdown.Menu>
                                <Dropdown.Item onClick={() => setActive(<FilterNameAsc/>)}>A...Z</Dropdown.Item>
                                <Dropdown.Item onClick={() => setActive(<FilterNameDesc order = 'desc'/>)}>Z...A</Dropdown.Item>
                            </Dropdown.Menu>
                        </Dropdown>
                    </Menu>
                    <GetProduct/>
                </Container>
                {active}
            </Tab.Pane>
        },
        {
            menuItem: 'WishList', render: () => <Tab.Pane active={isAuth}><Wishlist /></Tab.Pane>
        },
        {
            menuItem: 'Cart', render: () => <Tab.Pane active={isAuth}><Cart/></Tab.Pane>
        },
        {
            menuItem: 'Profile', render: () => <Tab.Pane active={isAuth}><Profile /></Tab.Pane>
        },
        {
            menuItem: 'Dashboard', render: () => <Tab.Pane active={isAuth}><Dashboard/></Tab.Pane>
        },
        {
            menuItem: 'My Orders', render: () => <Tab.Pane active={isAuth}><Orders/></Tab.Pane>
        },
        {
            menuItem: 'Admin', render: () => <Tab.Pane active={isAuth}>
                <container>
                    <Button onClick={() => setAdminActive(<CreateProduct/>)}>Create Product</Button>
                    <Button onClick={() => setAdminActive(<UpdateProduct/>)}>Update Product</Button>
                    <Button onClick={() => setAdminActive(<DeleteProduct/>)}>Delete Product</Button>
                </container>
                {adminActive}</Tab.Pane>
        }
    ]

    return (
        <div>
            <p />
            <div align='right' >
                <Modal
                    basic
                    onClose={() => setOpen(false)}
                    onOpen={() => setOpen(true)}
                    open={open}
                    size='small'
                    trigger={<Button align='right'>Log out</Button>}
                >
                    <Header as='h2' icon>
                        <Icon name='archive' />
                        Are you sure?
                    </Header>
                    <Modal.Content align='center'>
                        <p>
                            Are you sure you want to log out?
                        </p>
                        <Modal.Actions align='center'>
                            <Button className='exit red' color='red' inverted onClick={() => setOpen(false)}>
                                <Icon name='remove' /> No, I do not want to log out
                            </Button>
                            <Button className='exit green' color='green' inverted onClick={handleLogOut}>
                                <Icon name='checkmark' /> Yes, I want to log out
                            </Button>
                        </Modal.Actions>
                    </Modal.Content>
                </Modal>
            </div>
            {userType === 'regular'?
                (<Tab panes={panes}/>) :
                (<Tab panes={userPanes} />)}


        </div>
    )

}
export default CheckingAuth;
