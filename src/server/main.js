const express = require('express');
const path = require('path');
const pshell = require('python-shell');

const app = express();
const solverpath = 'sudoku-solver.py'
path.resolve(__dirname, 'sudoku-solver.py')


// respond with "hello world" when a GET request is made to the homepage
app.get('/solve', function (req, res) {
    const args = [req.query.table];
    pshell.run(solverpath, { args, scriptPath: __dirname, mode: 'json' }, (err, results) => {
        if (err || !results.length) {
            console.log(err);
            return res.json({status: 'error'});
        }
        console.log(results);
        res.json({
            status: 'ok',
            result: results[0]
        });
    });
});

app.use(express.static(path.resolve(__dirname, '../../build')));

app.listen(3000, function () {
    console.log('Listening on port 3000');
});
