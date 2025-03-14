//validate new launch input
//return launchmodl.createlaunch status code

const Launch = require("./Launch");

class LaunchController {
    
    constructor(model){
        this.model = model;
    }

    createLaunch( inputLaunch ) {
        if ( this.isValidLaunch( inputLaunch ) ) {
            console.log("Launch input is valid");
            return this.model.createLaunch( inputLaunch );
        }
        return 0;
    }
    
    
    isValidLaunch( inputLaunch ) {    
        if ( !this.isValidString( inputLaunch.name ) || !this.isValidString( inputLaunch.loc)
            || !this.isValidDate( inputLaunch.date )
            || !this.isValidTime( inputLaunch.time )
            || isNaN( inputLaunch.altitude ) || isNaN( inputLaunch.temp) || isNaN( inputLaunch.weight)) {
                console.log("Launch input is invalid");
                // return false;
            }

        if (isNaN(inputLaunch.altitude) || isNaN(inputLaunch.temp) || isNaN(inputLaunch.weight)) {
            console.log(inputLaunch.altitude);
            console.log(inputLaunch.temp);
            console.log(inputLaunch.weight);
            return false;
        }
        return true;
    }
    
    //accepts a-z A-Z 0-9 whitespace .,!?'"- undefined
    isValidString( input ) {
        let valid = ( typeof input === 'string' && /^[a-zA-Z0-9\s.,!?'"-]*$/.test( input ) ) || input === undefined;
        console.log("String valid: " + valid);
        return valid;
    }
    
    //TODO
    isValidDate( input ) {
        //react should handle date validation, not checking here due to time constraints. 
        //open to coming up with a better solution later on.
        return true;
    }
    
    //TODO
    isValidTime( input ) {
        //react should handle time validation, not checking here due to time constraints.
        //open to coming up with a better solution later on.
        return true;
    }
    
    //return -1 if invalid input
    //return 0 if not found
    //return a launch by the given name if found
    readLaunch( inputName ) {
    
        if ( !isValidString( inputName ) ) {
    
            return -1;
        }
        return this.model.readLaunch( inputName );
    }
    
    //parameter: a launch struct with values to update, all other fields undefined
    //return -1 if invalid input
    //return 0 if not found
    //return 1 if successful update
    updateLaunch( inputLaunch ) {
    
        if ( !isValidLaunch( inputLaunch ) ) {
    
            return -1;
        }
        return this.model.updateLaunch( inputLaunch ); 
    }
    
    //return -1 if invalid input
    //return 0 if not found
    //return 1 if successfully deleted
    deleteLaunch( inputName ) {
    
        if ( !isValidString( inputName ) ) {
    
            return -1;
        }
        return this.model.deleteLaunch( inputName );
    }
}

module.exports = LaunchController;