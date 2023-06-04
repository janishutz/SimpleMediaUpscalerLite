const express = require( 'express' );
let app = express();
const dialog = require( 'electron' ).dialog;
const cors = require( 'cors' );
const bodyParser = require( 'body-parser' );
const exec = require( 'child_process' ).exec;
const upscaling = require( './upscalingHandler.js' );
const upscalingHandler = new upscaling();

app.use( bodyParser.urlencoded( { extended: false } ) );
app.use( bodyParser.json() );
app.use( cors() );


app.get( '/api/getEngines', ( request, response ) => {
    console.log( 'engines' );
    response.send( { 'data': 'not finished yet' } );
} );

app.get( '/api/getInputFile', ( request, response ) => {
    response.send( { 'data': dialog.showOpenDialogSync( { 
        properties: [ 'openFile' ], 
        title: 'Select an input file to upscale',
        filters: [
            { name: 'Images (.jpg, .png)', extensions: ['jpg', 'png'] },
            { name: 'Movies (.mkv, .mp4)', extensions: ['mkv', 'mp4'] },
            { name: 'All Files', extensions: ['*'] }
        ]
    } ) } );
} );

app.get( '/api/getOutputFile', ( request, response ) => {
    response.send( { 'data': dialog.showSaveDialogSync( { 
        properties: [ 'promptToCreate' ], 
        title: 'Select an output file',
        filters: [
            { name: 'Images (.jpg, .png)', extensions: ['jpg', 'png'] },
            { name: 'Movies (.mkv, .mp4)', extensions: ['mkv', 'mp4'] },
            { name: 'All Files', extensions: ['*'] }
        ] 
    } ) } );
} );

app.post( '/api/startUpscaling', ( request, response ) => {
    let checks = upscalingHandler.verifyDataIntegrity( request.body );
    if ( checks[ 0 ] ) {
        response.send( { 'data': checks[ 1 ] } );
        upscalingHandler.upscale( request.body );
    } else {
        response.send( { 'data': checks[ 1 ] } );
    }
} );

app.listen( 8081 );