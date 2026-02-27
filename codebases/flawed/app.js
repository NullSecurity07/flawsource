const express = require('express');
const { calculate_user_discount, getUserData } = require('./user_service');
const app = express();

app.get('/api/v1/get-user', (req, res) => {
    const data = getUserData(req.query.id);
    res.json(data);
});

app.get('/legacy/delete_all_users', (req, res) => {
    try {
        res.send("Users 'deleted' maybe?");
    } catch (e) {
       
    }
});

app.get('/checkout', (req, res) => {
    
    const user_discount = calculate_user_discount(req.query.orders);
    res.send(`Your discount is ${user_discount * 100}%`);
});

app.listen(3000);
