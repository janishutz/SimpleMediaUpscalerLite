module.exports = function ( win ) {
    const dialog = require( 'electron' ).dialog;
    const upscaling = require( './upscalingHandler.js' );
    const upscalingHandler = new upscaling();
    const ipcMain = require( 'electron' ).ipcMain;

    ipcMain.on( 'selectInputFile', ( event, data ) => {
        event.reply( 'selectInputFile', { 'data': dialog.showOpenDialogSync( { 
            properties: [ 'openFile' ], 
            title: 'Select an input file to upscale',
            filters: [
                { name: 'Images (.jpg, .png)', extensions: ['jpg', 'png'] },
                { name: 'Movies (.mkv, .mp4)', extensions: ['mkv', 'mp4'] },
                { name: 'All Files', extensions: ['*'] }
            ]
        } ) } );
    } );

    ipcMain.on( 'selectOutputFile', ( event, data ) => {
        event.reply( 'selectOutputFile', { 'data': dialog.showSaveDialogSync( { 
            properties: [ 'promptToCreate' ], 
            title: 'Select an output file',
            filters: [
                { name: 'Images (.jpg, .png)', extensions: ['jpg', 'png'] },
                { name: 'Movies (.mkv, .mp4)', extensions: ['mkv', 'mp4'] },
                { name: 'All Files', extensions: ['*'] }
            ] 
        } ) } );
    } );

    ipcMain.on( 'startUpscaling', ( event, data ) => {
        let checks = upscalingHandler.verifyDataIntegrity( JSON.parse( data ), ipcMain );
        if ( checks[ 0 ] ) {
            event.reply( 'startUpscaling', { 'data': checks[ 1 ] } );
            upscalingHandler.upscale( JSON.parse( data ), win );
        } else {
            event.reply( 'startUpscaling', { 'data': checks[ 1 ] } );
        }
    } );
}