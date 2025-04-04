/*
    class: Launch

    members:    String name
                number date
                number time
                List<String> parameterNames
                List<number> parameterValues
                number[][][] data

    methods:    constructor()
                static fromjson(jsonstring)

    purpose:    Data structure for a launch, to be used throughout the backend.
*/

class Launch {

    /*  
        function: constructor

        params: String name
                number date
                number time
                List<String> parameterNames
                List<number> parameterValues

        purpose: returns a new Launch data object with null data
    */
    constructor( name, date, time, loc, altitude, temp, weight ) {

        this.name = name;
        this.date = date;
        this.time = time;
        this.loc = loc;
        this.altitude = altitude;
        this.temp = temp;
        this.weight = weight;
        // this.parameterNames = parameterNames;
        // this.parameterValues = parameterValues;
        this.data = null;
    }

    // static fromjson(jsonstring){
    //     let obj = JSON.parse(jsonstring);
    //     return new Launch(obj.name, obj.date, obj.time, obj.parameterNames, obj.parameterValues);

    //     //example usage: obj launch = Launch.fromjson(jsonstring);
    // }
}

module.exports = Launch;