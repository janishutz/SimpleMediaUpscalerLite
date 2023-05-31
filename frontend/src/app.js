const express = require( 'express' );
let app = express();
const path = require( 'path' );
const fs = require( 'fs' );
const bodyParser = require( 'body-parser' );
const exec = require( 'child_process' ).exec;

app.use( bodyParser.urlencoded( { extended: false } ) );
app.use( bodyParser.json() );

function execute(command, callback){
    exec(command, function(error, stdout, stderr){ callback(stdout); });
};

app.get( '/api/getEngines', ( request, response ) => {
    execute( 'ImageVideoUpscaler-cli -p', out => {
        response.send( out );
    } );
} );

app.listen( 8081 );