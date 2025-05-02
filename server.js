const LaunchModel = require('./LaunchModel.js');
const LaunchController = require('./LaunchController.js');

const model = new LaunchModel();
const controller = new LaunchController(model);

const express = require('express');

var cors = require('cors');
var app = express();

app.use(cors())

const { openSync } = require('fs');
const { readFileSync } = require('fs');

// const corsOptions = {
//     origin: ["http://localhost:3001"]
// }

// app.use(cors(corsOptions));

app.use(express.static('public'));

app.listen(3000, () => {console.log('Server running on port 3000')});

app.post('/', express.json(), (req, res, next) => {
    console.log(req.body);
    res.sendStatus(200);

    var launch_obj = controller.createLaunch(req.body);

    // var launch_obj = LaunchController.createLaunch(req.body);
    // console.log(launch_obj);
});

//read '/List of Launch Sites/output.json' and send it to the client

f = openSync('List of Launch Sites/output.json', 'r');
const data = readFileSync(f);
const jsonData = JSON.parse(data);

app.get('/sites', (req, res) => {
    console.log("/sites GET request received");
    res.send(jsonData);
});

app.post('/rank', express.json(), (req, res) => {

    json_message = req.body;
    console.log(json_message);
    
    // dont need this shit just have client send request directly to api.


});