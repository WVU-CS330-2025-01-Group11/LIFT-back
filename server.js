const LaunchModel = require('./LaunchModel.js');
const LaunchController = require('./LaunchController.js'); // similar export for LaunchController

const model = new LaunchModel();
const controller = new LaunchController(model);

const express = require('express');
const app = express();
const cors = require('cors');

const corsOptions = {
    origin: ["http://localhost:3001"]
}

app.use(cors(corsOptions));

app.use(express.static('public'));

app.listen(3000, () => {console.log('Server running on port 3000')});

app.post('/', express.json(), (req, res, next) => {
    console.log(req.body);
    res.sendStatus(200);

    var launch_obj = controller.createLaunch(req.body);

    // var launch_obj = LaunchController.createLaunch(req.body);
    // console.log(launch_obj);
});