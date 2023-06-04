/*
*				ImageVideoUpscaler - upscalingHandler.js
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

    upscale( options, io ) {
        // required options: engine, algorithm, scale, sharpening, InputFile & OutputFile
        // Options is an object!

        let baseCommand = '';
        // Create cli command to upscale
        if ( this.os === 'linux' ) {
            baseCommand = './imagevideoupscaler';
        } else if ( this.os === 'win32' ) {
            baseCommand = 'imagevideoupscaler';
        }

        
        let args = []
        args.push( '-i' + options.InputFile );
        args.push( '-o ' + options.OutputFile );
        
        args.push( '-s ' + options.scale )
        
        // add additional options
        // baseCommand +=  + ' -S ' + options.sharpening
        // baseCommand += ' -E ' + options.engine + ' -M ' + options.algorithm
        
        let child = child_process.spawn( baseCommand, args );
        
        child.stdout.on( 'data', data => {
            console.log( '' + data );
            io.emit( 'progress', '\n' + data );
        } );
        
        child.stderr.on( 'data', ( data ) => {
            console.error(`stderr: ${ data }`);
        } );
        
        child.on( 'error', ( error ) => {
            new Notification( { title: `ImageVideoUpscaler - Error whilst upscaling', body: 'Your upscaling Job encountered an error whilst upscaling. (Error message: ${ error.message }).`} )
        } );
        
        child.on( 'close', ( code ) => {
            new Notification( { title: `ImageVideoUpscaler - Job complete', body: 'Your Upscaling job has completed successfully (Code ${ code }). You may find its output here: ` + options.OutputFile } )
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