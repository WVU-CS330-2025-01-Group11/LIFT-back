
let launches = new Array();

/*
    function:   createNewLaunch

    parameter:  Object inputLaunch {
    
                        String name
                        number date
                        number time
                        List<String> parameterNames
                        List<number> parameterValues
                    }

    purpose:    creates a new Launch data object.
                executes rank() on that Launch
                stores the Launch in the database

    returns:    0: failure
                1: success
*/
function createNewLaunch( inputLaunch ) {

    var newLaunch = new Launch( inputLaunch.name,
                                inputLaunch.date,
                                inputLaunch.time,
                                inputLaunch.parameterNames,
                                inputLaunch.parameterValues );
    //rank( newLaunch );
    if ( launches.push( newLaunch ) > 0 ) {

        return 1;
    } 
    return 0;    
}

function updateLaunch( inputLaunch ) {

    //check if the launch exists
    //if not, return 2
    //if so, grab the old launch
    //declare a new launch
    //for each field in inputLaunch
        //if the field is empty
            //put the old field in the new launch
        //else
            //put inputLaunch's field in the new launch
    //delete old launch
    //add new launch
    //if launches got bigger
        //return 1
    //return 0

    //grab old launch, return an error code if it doesn't exist yet
    var oldLaunch = launches.find( launch => launch.name === inputLaunch.name );
    if ( oldLaunch == undefined ) {

        return 2;
    }

    //populate the new launch's fields
    //if any inputLaunch field is empty, use the value of the oldLaunch's field to make sure all fields have a value
    let newLaunch = oldLaunch;
    const inputKeys = inputLaunch.keys();
    inputKeys.foreach( key => {

        if ( inputLaunch[ key ] == undefined ) {

            newLaunch[ key ] = oldLaunch[ key ];
        } else {

            newLaunch[ key ] = inputLaunch[ key ];
        }
    } );

    //replace old launch with new launch
    //TODO: REPLACE OLD LAUNCH WITH NEW LAUNCH
}

/*
    class: Launch

    members:    String name
                number date
                number time
                List<String> parameterNames
                List<number> parameterValues
                number[][][] data

    purpose:    stores data about a launch event
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
    constructor( name, date, time, parameterNames, parameterValues ) {

        this.name = name;
        this.date = date;
        this.time = time;
        this.parameterNames = parameterNames;
        this.parameterValues = parameterValues;
        this.data = null;
    }
}




