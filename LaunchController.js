//validate new launch input
//return launchmodl.createlaunch:
//  0 if fail
//  Launch if success
function createLaunch( inputLaunch ) {

    if ( isValidLaunch( inputLaunch ) ) {

        return LaunchModel.createLaunch( inputLaunch );
    }
    return 0;
}

function isValidLaunch( inputLaunch ) {

    if ( !isValidString( inputLaunch.name )
        || !isValidDate( inputLaunch.date )
        || !isValidTime( inputLaunch.time )
        || inputLaunch.parameterNames.some( name => !isValidString( name ) )
        || inputLaunch.parameterValues.some( value => isNaN( value ) ) ) {
        
            return false;
        }
    return true;
}

//accepts a-z A-Z 0-9 whitespace .,!?'"- undefined
function isValidString( input ) {

    return ( typeof input === 'string' && /^[a-zA-Z0-9\s.,!?'"-]*$/.test( input ) )
            || input === undefined;
}

//TODO
function isValidDate( input ) {

    return false;
}

//TODO
function isValidTime( input ) {

    return false;
}

//return -1 if invalid input
//return 0 if not found
//return a launch by the given name if found
function readLaunch( inputName ) {

    if ( !isValidString( inputName ) ) {

        return -1;
    }
    return LaunchModel.readLaunch( inputName );
}

//parameter: a launch struct with values to update, all other fields undefined
//return -1 if invalid input
//return 0 if not found
//return Launch if successful update
function updateLaunch( inputLaunch ) {

    if ( !isValidLaunch( inputLaunch ) ) {

        return -1;
    }
    return LaunchModel.updateLaunch( inputLaunch ); 
}

//return -1 if invalid input
//return 0 if not found
//return 1 if successfully deleted
function deleteLaunch( inputName ) {

    if ( !isValidString( inputName ) ) {

        return -1;
    }
    return LaunchModel.deleteLaunch( inputName );
}