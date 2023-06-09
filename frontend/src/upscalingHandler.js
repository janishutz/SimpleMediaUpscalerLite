/*
*				SimpleMediaUpscalerLite - upscalingHandler.js
*
*	Created by Janis Hutz 06/03/2023, Licensed under the GPL V3 License
*			https://janishutz.com, development@janishutz.com
*
*
*/

const child_process = require( 'child_process' );
const process = require( 'process' );
const Notification = require( 'electron' ).Notification;


class UpscalingHandler {
    constructor () {
        this.os = process.platform
    }

    upscale( options, win ) {
        // required options: engine, algorithm, scale, sharpening, InputFile & OutputFile
        // Options is an object!

        let baseCommand = '';
        // Create cli command to upscale
        if ( this.os === 'linux' ) {
            baseCommand = './smuL-cli';
        } else if ( this.os === 'win32' ) {
            baseCommand = 'smuL-cli.exe';
        }

        
        let args = []
        args.push( '-i' + options.InputFile );
        args.push( '-o' + options.OutputFile );
        
        if ( options.scale != 0 ) {
            args.push( '-s' + options.scale );
        }

        if ( options.sharpening != 0 ) {
            args.push( '-S' + options.sharpening );
        }

        args.push( '-M' + options.algorithm );
        args.push( '-E' + options.engine );
        // add additional options
        // baseCommand +=  + ' -S ' + options.sharpening
        // baseCommand += ' -E ' + options.engine + ' -M ' + options.algorithm

        console.log( 'upscaling' );

        console.log( args );
        
        let child = child_process.spawn( baseCommand, args );
        
        child.stdout.on( 'data', data => {
            console.log( '' + data );
            win.send( 'progress', '\n' + data );
        } );
        
        child.stderr.on( 'data', ( data ) => {
            console.error(`stderr: ${ data }`);
        } );
        
        child.on( 'error', ( error ) => {
            console.log( 'An error occurred' + error );
            win.send( 'error', 'An error occurred during upscaling. (Error message: ' + error.message + ')' );
            new Notification( { title: `SimpleMediaUpscalerLite - Error whilst upscaling', body: 'Your upscaling Job encountered an error whilst upscaling. (Error message: ${ error.message }).`} ).show();
        } );
        
        child.on( 'close', ( code ) => {
            win.send( 'finish', 'Your upscaling job finished with exit code ' + code + '. You may find its output here: ' + options.OutputFile  );
            new Notification( { title: `SimpleMediaUpscalerLite - Job complete', body: 'Your Upscaling job has completed successfully (Code ${ code }). You may find its output here: ` + options.OutputFile } ).show();
        } );
    }

    verifyDataIntegrity ( data ) {
        if ( data[ 'InputFile' ] && data[ 'OutputFile' ] && data[ 'engine' ] && data[ 'algorithm' ] && 1 < data[ 'scale' ] <= 4 && 0 <= data[ 'sharpening' ] <= 1 ) {
            if ( data[ 'InputFile' ][ 0 ].substring( data[ 'InputFile' ][ 0 ].length - 4 ) == data[ 'OutputFile' ].substring( data[ 'OutputFile' ].length - 4 ) ) {
                return [ true, 'upscaling' ];
            } else { 
                return [ false, 'differentFileExtensions' ]; 
            }
        } else {
            return [ false, 'dataMissing' ];
        };
    }
}

module.exports = UpscalingHandler;