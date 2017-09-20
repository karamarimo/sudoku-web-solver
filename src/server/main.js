const express = require('express');
const path = require('path');
const app = express();

// respond with "hello world" when a GET request is made to the homepage
app.get('/solve', function (req, res) {
    res.json({
        result: 321
    });
});

app.use(express.static(path.resolve(__dirname, '../../build')));

app.listen(3000, function () {
    console.log('Listening on port 3000');
});
