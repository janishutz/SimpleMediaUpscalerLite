/*
*				ImageVideoUpscaler - upscalingHandler.js
*
*	Created by Janis Hutz 06/03/2023, Licensed under the GPL V3 License
*			https://janishutz.com, development@janishutz.com
*
*
*/

const exec = require( 'child_process' ).exec;
const process = require( 'process' );

function execute(command, callback){
    exec(command, function(error, stdout, stderr){ callback(stdout); });
};

class UpscalingHandler {
    constructor () {
        this.os = process.platform
    }

    upscale( options ) {
        // required options: engine, algorithm, scale, sharpening, InputFile & OutputFile
        // Options is an object!

        let baseCommand = '';
        // Create cli command to upscale
        if ( this.os === 'linux' ) {
            baseCommand = './imagevideoupscaler -i ';
        } else if ( this.os === 'win32' ) {
            baseCommand = 'imagevideoupscaler -i ';
        }

        baseCommand += options.InputFile + ' -o ' + options.OutputFile

        // add additional options
        baseCommand += ' -s ' + options.scale + ' -S ' + options.sharpening
        baseCommand += ' -E ' + options.engine + ' -M ' + options.algorithm

        execute( baseCommand, out => {
            console.log( out );
        } );
    }

    verifyDataIntegrity ( data ) {
        if ( data[ 'InputFile' ] && data[ 'OutputFile' ] && data[ 'engine' ] && data[ 'algorithm' ] && 1 < data[ 'scale' ] <= 4 && 0 <= data[ 'sharpening' ] <= 1 ) {
            return true;
        } else {
            return false;
        };
    }
}

module.exports = UpscalingHandler;