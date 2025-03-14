const Launch = require( './Launch.js' );

class LaunchModel {

    constructor() {
        //array of Launch objects
        this.launches = new Array();
    }

    /*
        function:   createLaunch

        parameter:  json string

        purpose:    creates a new Launch data object.
                    executes rank() on that Launch
                    stores the Launch in the database

        returns:    0: failure
                    1: success
    */
    createLaunch( inputLaunch ) {
        var newLaunch = new Launch( inputLaunch.name,
                                    inputLaunch.date,
                                    inputLaunch.time,
                                    inputLaunch.loc,
                                    inputLaunch.altitude,
                                    inputLaunch.temp,
                                    inputLaunch.weight ); 
        
        newLaunch = this.rank( newLaunch );
        if ( this.launches.push( newLaunch ) > 0 ) {
    
            console.log( "Launch added to model successfully" );
            console.log( this.launches.length, "launches in model" );
            console.log( this.launches );
            return 1;
        } 
        return 0;
    }

    updateLaunch( inputLaunch ) {

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

    //PLACEHOLDER METHOD
    //assigns input.data = "ranked placeholder" and returns input
    rank( inputLaunch ) {
        inputLaunch.data = "ranked placeholder";
        return inputLaunch;
    }

    //returns index of the launch in launches if it exists
    //return -1 otherwise
    getLaunchIndex( inputName ) {

        return launches.findIndex( inputName );
    }

    //returns 0 if launch not found
    //returns launch if found
    readLaunch( inputName ) {

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
    deleteLaunch( inputName ) {
        //check if it exists, throw if not
        let index = getLaunchIndex( inputName );
        if ( index == -1 ) {

            return 0;
        }

        //delete the launch and return 1 if it exists
        launches.splice( index, 1 );
        return 1;
    }
}

module.exports = LaunchModel