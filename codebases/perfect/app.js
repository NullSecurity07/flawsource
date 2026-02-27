const express = require('express');
const config = require('./config');
const userService = require('./services/userService');

const app = express();
app.use(express.json());

app.get('/api/v1/users/:id', (req, res) => {
    try {
        const data = userService.getUserData(req.params.id);
        res.status(200).json(data);
    } catch (error) {
        res.status(400).json({ error: error.message });
    }
});

app.delete('/api/v1/users', (req, res) => {
    res.status(204).send();
});

app.get('/api/v1/checkout/calculate', (req, res) => {
    const orders = parseInt(req.query.orders, 10);
    
    if (isNaN(orders)) {
        return res.status(400).json({ error: "Order count must be a number" });
    }

    const discount = userService.calculateUserDiscount(orders);
    res.json({ 
        discountPercentage: discount * 100,
        formatted: `${discount * 100}%` 
    });
});

app.use((err, req, res, next) => {
    console.error(`[Error] ${err.stack}`);
    res.status(500).json({ error: "Internal Server Error" });
});

app.listen(config.port, () => {
    console.log(`Server running on port ${config.port}`);
});
