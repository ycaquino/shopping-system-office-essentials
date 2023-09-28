import React, {Component, useEffect, useState} from 'react';
import {Button, Card, Container, Modal, Header, Grid, GridRow, CardHeader, CardContent, GridColumn, Divider} from "semantic-ui-react";
import {Icon} from "semantic-ui-react";
import {Bar, BarChart, CartesianGrid, Legend, Tooltip, XAxis, YAxis} from "recharts";
import axios from "axios";
import * as storeData from "store";

function CheckingAuth() {
    if(typeof storeData.get('id') === 'undefined'){
        return (<Container align='center'>
            <Header>Access denied.</Header>
            <Divider />
            <Button content="Click here to be redirected to Log-In" onClick={(event => {window.location = '/Home'})}/>
        </Container>)
    }

    else {
        return <Dashboard />
    }

}


function Dashboard() {
    let dataUser = storeData.get('id');
    // const [data, setData] = useState([{"name": 1, "Counts": 5},
    //     {"name": 2, "Counts": 4},
    //     {"name": 3, "Counts": 3},
    //     {"name": 4, "Counts": 2},
    //     {"name": 5, "Counts": 1}]);

    const [expensiveG, setExpensiveG] = useState([])
    const [cheapestG, setCheapestG] = useState([])
    const [mostLikedG, setMostLikedG] = useState([])
    const [expensiveU, setExpensiveU] = useState([])
    const [cheapestU, setCheapestU] = useState([])
    const [ranking5CategoriesG, setRanking5CategoriesG] = useState([])
    const [ranking10CategoriesG, setRanking10CategoriesG] = useState([])
    const [ranking5ProductG, setRanking5ProductG] = useState([])
    const [ranking10ProductG, setRanking10ProductG] = useState([])
    const [ranking5CategoriesU, setRanking5CategoriesU] = useState([])
    const [ranking10CategoriesU, setRanking10CategoriesU] = useState([])
    const [ranking5ProductU, setRanking5ProductU] = useState([])
    const [ranking10ProductU, setRanking10ProductU] = useState([])


    useEffect(() => {
        axios.get('https://office-essentials-app.herokuapp.com/office-essentials/products/global/most_expensive')
            .then(response => {
                setExpensiveG(response.data[0])
            }, error => {
                console.log(error);
            });

        axios.get('https://office-essentials-app.herokuapp.com/office-essentials/products/global/least_expensive')
            .then(response => {
                setCheapestG(response.data[0])
            }, error => {
                console.log(error);
            });



        axios.get('https://office-essentials-app.herokuapp.com/office-essentials/Wishlist/MostLiked')
            .then(response => {
                setMostLikedG(response.data)
            }, error => {
                console.log(error);
            });


        axios.post('https://office-essentials-app.herokuapp.com/office-essentials/User/HighestProduct/',{
        user_id: dataUser
    }, {
            headers: {
                // 'application/json' is the modern content-type for JSON, but some
                // older servers may use 'text/json'.
                // See: http://bit.ly/text-json
                'content-type': 'application/json'
            }})
            .then(response => {
                setExpensiveU(response.data)
            }, error => {
                console.log(error);
            });

        axios.post('https://office-essentials-app.herokuapp.com/office-essentials/User/LowestProduct/',{
            user_id: dataUser
        }, {
            headers: {
                // 'application/json' is the modern content-type for JSON, but some
                // older servers may use 'text/json'.
                // See: http://bit.ly/text-json
                'content-type': 'application/json'
            }})
            .then(response => {
                setCheapestU(response.data)
            }, error => {
                console.log(error);
            });


        axios.get('https://office-essentials-app.herokuapp.com/office-essentials/products/global/ranking_categories/5')
            .then(response =>{
                setRanking5CategoriesG(response.data)
            }, error => {
                console.log(error);
            });

        axios.get('https://office-essentials-app.herokuapp.com/office-essentials/products/global/ranking_categories/10')
            .then(response =>{
                setRanking10CategoriesG(response.data)
            }, error => {
                console.log(error);
            });

        axios.get('https://office-essentials-app.herokuapp.com/office-essentials/products/global/ranking_products/5')
            .then(response =>{
                setRanking5ProductG(response.data)
            }, error => {
                console.log(error);
            });

        axios.get('https://office-essentials-app.herokuapp.com/office-essentials/products/global/ranking_products/10')
            .then(response =>{
                setRanking10ProductG(response.data)
            }, error => {
                console.log(error);
            });



        axios.post('https://office-essentials-app.herokuapp.com/office-essentials/User/RankingCategories/5',{
            user_id: dataUser
        }, {
            headers: {
                'content-type': 'application/json'
            }})
            .then(response => {
                setRanking5CategoriesU(response.data)
            }, error => {
                console.log(error);
            });

        axios.post('https://office-essentials-app.herokuapp.com/office-essentials/User/RankingCategories/10',{
            user_id: dataUser
        }, {
            headers: {
                'content-type': 'application/json'
            }})
            .then(response => {
                setRanking10CategoriesU(response.data)
            }, error => {
                console.log(error);
            });

        axios.post('https://office-essentials-app.herokuapp.com/office-essentials/User/RankingProduct/5',{
            user_id: dataUser
        }, {
            headers: {
                'content-type': 'application/json'
            }})
            .then(response => {
                setRanking5ProductU(response.data)
            }, error => {
                console.log(error);
            });

        axios.post('https://office-essentials-app.herokuapp.com/office-essentials/User/RankingProduct/10',{
            user_id: dataUser
        }, {
            headers: {
                'content-type': 'application/json'
            }})
            .then(response => {
                setRanking10ProductU(response.data)
            }, error => {
                console.log(error);
            });
        }, [])




    return <Container>
        <Header as='h2' textAlign='center' className='dash'>
            Global Statistics
        </Header>
        <Grid align='center' columns='equal'>
            <GridRow columns='equal'>
                <Grid.Column>
                    <Card>
                        <CardHeader className='card-header'>Most Expensive Product</CardHeader>
                        <CardContent>
                            <Icon name='chevron up'/>
                            <p>Product Name: {expensiveG.product_name}</p>
                            <p>Product Category: {expensiveG.product_category}</p>
                            <p>Product Price: {expensiveG.product_price}</p>
                        </CardContent>
                    </Card>
                </Grid.Column>
                <Grid.Column>
                    <Card>
                        <CardHeader className='card-header'>Least Expensive Product</CardHeader>
                        <CardContent>
                            <Icon name='chevron down'/>
                            <p>Product Name: {cheapestG.product_name}</p>
                            <p>Product Category: {cheapestG.product_category}</p>
                            <p>Product Price: {cheapestG.product_price}</p>
                        </CardContent>
                    </Card>
                </Grid.Column>
                <GridColumn>
                    <Card>
                        <CardHeader className='card-header'>Most Liked Product</CardHeader>
                        <CardContent>
                            <Icon position='left' name='thumbs up'/>
                            <p>Product Name: {mostLikedG.product_name}</p>
                            <p>Product Category: {mostLikedG.product_category}</p>
                            <p>Product Price: {mostLikedG.product_price}</p>
                        </CardContent>
                    </Card>
                </GridColumn>
            </GridRow>
        </Grid>

        <Header as='h3' textAlign='center' className='dash'>
            Top Categories
        </Header>
        <Grid>
            <GridRow align='center' columns='equal'>
                <Grid.Column>
                    <Card fluid={true}>
                        <CardHeader>
                            Top 5
                        </CardHeader>
                        <BarChart align='center' width={500} height={150} data={ranking5CategoriesG}>
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="product_category" />
                            <YAxis />
                            <Tooltip />
                            <Legend />
                            <Bar dataKey="count" fill="#8884d8"/>
                        </BarChart>
                    </Card>
                </Grid.Column>
                <Grid.Column>
                    <Card fluid={true}>
                        <Card fluid={true}>
                            <CardHeader>
                                Top 10
                            </CardHeader>
                            <BarChart align='center' width={500} height={150} data={ranking10CategoriesG}>
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis dataKey="product_category" />
                                <YAxis />
                                <Tooltip />
                                <Legend />
                                <Bar dataKey="count" fill="#8884d8"/>
                            </BarChart>
                        </Card>
                    </Card>
                </Grid.Column>
            </GridRow>
        </Grid>
        <Header as='h3' textAlign='center' className='dash'>
            Top Products
        </Header>
        <Grid>
            <GridRow align='center' columns='equal'>
                <Grid.Column>
                    <Card fluid={true}>
                        <CardHeader>
                            Top 5
                        </CardHeader>
                        <BarChart align='center' width={500} height={150} data={ranking5ProductG}>
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="product_category" />
                            <YAxis />
                            <Tooltip />
                            <Legend />
                            <Bar dataKey="count" fill="#8884d8"/>
                        </BarChart>
                    </Card>
                </Grid.Column>
                <Grid.Column>
                    <Card fluid={true}>
                        <Card fluid={true}>
                            <CardHeader>
                                Top 10
                            </CardHeader>
                            <BarChart align='center' width={500} height={150} data={ranking10ProductG}>
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis dataKey="product_category" />
                                <YAxis />
                                <Tooltip />
                                <Legend />
                                <Bar dataKey="count" fill="#8884d8"/>
                            </BarChart>
                        </Card>
                    </Card>
                </Grid.Column>
            </GridRow>
        </Grid>
        <Header as='h2' textAlign='center' className='dash'>
            Personal Statistics
        </Header>
        <Grid align='center' columns='equal'>
            <GridRow columns='equal'>
                <GridColumn>
                    <Card>
                        <CardHeader className='card-header'>
                            Most Expensive Product Bought
                        </CardHeader>
                        <CardContent>
                            <Icon name='chevron up'/>
                            <p>Product Name: {expensiveU.product_name}</p>
                            <p>Product Category: {expensiveU.product_category}</p>
                            <p>Product Price: {expensiveU.product_price}</p>
                        </CardContent>
                    </Card>
                </GridColumn>
                <GridColumn>
                    <Card>
                        <CardHeader className='card-header'>
                            Least Expensive Product Bought
                        </CardHeader>
                        <CardContent>
                            <Icon name='chevron down'/>
                            <p>Product Name: {cheapestU.product_name}</p>
                            <p>Product Category: {cheapestU.product_category}</p>
                            <p>Product Price: {cheapestU.product_price}</p>
                        </CardContent>
                    </Card>
                </GridColumn>
            </GridRow>
        </Grid>
        <Header as='h3' textAlign='center' className='dash'>
            Top Categories
        </Header>
        <Grid>
            <GridRow align='center' columns='equal'>
                <Grid.Column>
                    <Card fluid={true}>
                        <CardHeader>
                            Top 5
                        </CardHeader>
                        <BarChart align='center' width={500} height={150} data={ranking5CategoriesU}>
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="product_category" />
                            <YAxis />
                            <Tooltip />
                            <Legend />
                            <Bar dataKey="count" fill="#8884d8"/>
                        </BarChart>
                    </Card>
                </Grid.Column>
                <Grid.Column>
                    <Card fluid={true}>
                        <Card fluid={true}>
                            <CardHeader>
                                Top 10
                            </CardHeader>
                            <BarChart align='center' width={500} height={150} data={ranking10CategoriesU}>
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis dataKey="product_category" />
                                <YAxis />
                                <Tooltip />
                                <Legend />
                                <Bar dataKey="count" fill="#8884d8"/>
                            </BarChart>
                        </Card>
                    </Card>
                </Grid.Column>
            </GridRow>
        </Grid>
        <Header as='h3' textAlign='center' className='dash'>
            Top Products
        </Header>
        <Grid>
            <GridRow align='center' columns='equal'>
                <Grid.Column>
                    <Card fluid={true}>
                        <CardHeader>
                            Top 5
                        </CardHeader>
                        <BarChart align='center' width={500} height={150} data={ranking5ProductU}>
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="product_name" />
                            <YAxis />
                            <Tooltip />
                            <Legend />
                            <Bar dataKey="amount" fill="#8884d8"/>
                        </BarChart>
                    </Card>
                </Grid.Column>
                <Grid.Column>
                    <Card fluid={true}>
                        <Card fluid={true}>
                            <CardHeader>
                                Top 10
                            </CardHeader>
                            <BarChart align='center' width={500} height={150} data={ranking10ProductU}>
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis dataKey="product_name" />
                                <YAxis />
                                <Tooltip />
                                <Legend />
                                <Bar dataKey="amount" fill="#8884d8"/>
                            </BarChart>
                        </Card>
                    </Card>
                </Grid.Column>
            </GridRow>
        </Grid>
    </Container>


}
export default CheckingAuth;