
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
                ranked Launch object: success
*/
function createLaunch( inputLaunch ) {

    var newLaunch = new Launch( inputLaunch.name,
                                inputLaunch.date,
                                inputLaunch.time,
                                inputLaunch.parameterNames,
                                inputLaunch.parameterValues );
    newLaunch = rank( newLaunch );
    if ( launches.push( newLaunch ) > 0 ) {

        return newLaunch;
    } 
    return 0;    
}



//TODO METHOD DOC

/*

*/
function updateLaunch( inputLaunch ) {

    //grab old launch, return an error code if it doesn't exist yet
    var oldLaunch = launches.find( launch => launch.name === inputLaunch.name );
    if ( oldLaunch == undefined ) {

        return 0;
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

    //delete old launch, update new launch's rankings, insert new launch, return 1
    deleteLaunch( oldLaunch.name );
    newLaunch = rank( newLaunch );
    launches.put( newLaunch );
    return 1;
}

/*
    class: Launch

    members:    String name
                number date
                number time
                List<String> parameterNames
                List<number> parameterValues
                number[][][] data

    methods:    constructor()

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

//PLACEHOLDER METHOD
//assigns input.data = -42 and returns input
function rank( inputLaunch ) {

    inputLaunch.data = -42;
    return inputLaunch;
}

//returns index of the launch in launches if it exists
//return -1 otherwise
function getLaunchIndex( inputName ) {

    return launches.findIndex( inputName );
}

//returns 0 if launch not found
//returns launch if found
function readLaunch( inputName ) {

    //guard condition
    let index = getLaunchIndex( inputName );
    if ( index == -1 ) {

        return 0;
    }

    //return the object if it exists
    return launches[ index ];
}

//returns 0 if launch not found
//returns 1 if launch successfully deleted
function deleteLaunch( inputName ) {

    //check if it exists, throw if not
    let index = getLaunchIndex( inputName );
    if ( index == -1 ) {

        return 0;
    }

    //delete the launch and return 1 if it exists
    launches.splice( index, 1 );
    return 1;
}

