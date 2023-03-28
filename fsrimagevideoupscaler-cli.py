"""
*				FSRImageVideoUpscalerFrontend - fsrimagevideoupscaler-cli.py
*
*	Created by Janis Hutz 03/15/2023, Licensed under the GPL V3 License
*			https://janishutz.com, development@janishutz.com
*
*
"""

import argparse
import bin.handler
import os
import multiprocessing

ap = argparse.ArgumentParser( description='FSRImageVideoUpscaler - CLI, a CLI application to upscale videos and images using FSR. ' )
ap.add_argument( 'inputfile', help='File path for the video / image to be upscaled' )
ap.add_argument( 'outputfile', help='File path for the video / image that was upscaled' )
ap.add_argument( '-s', '--scalefactor', help='Scale factor for the video / image' )
ap.add_argument( '-T', '--threads', help='Thread count to use. Cannot exceed CPU thread count. Scaling non-linear (using 2 threads is not exactly 2x the speed of 1 thread)' )
args = ap.parse_args()

handler = bin.handler.Handler()

go = True;

if __name__ == '__main__':
    multiprocessing.freeze_support();
    if ( os.path.exists( args.outputfile ) ):
        if ( input( 'File already exists. Do you want to replace it? (y/n) ' ).lower() == 'y' ):
            go = True
            os.remove( args.outputfile );
        else:
            print( '\nRefusing to Upscale video. Please delete the file or specify another filepath!')
            go = False

    if ( go ):
        if ( args.scalefactor ):
            if ( args.scalefactor[ len(args.scalefactor) -1: ] == 'x' ):
                if ( args.threads != None ):
                    handler.handler( 'bin/lib/FidelityFX_CLI.exe', args.inputfile, 'custom', args.scalefactor, args.outputfile, threads=int( args.threads ) );
                else:
                    handler.handler( 'bin/lib/FidelityFX_CLI.exe', args.inputfile, 'custom', args.scalefactor, args.outputfile );
            else:
                raise NameError( 'Argument Scale does require to be of form 2x! (it has to end in x)' )
        else:
            if ( args.threads != None ):
                handler.handler( 'bin/lib/FidelityFX_CLI.exe', args.inputfile, 'custom', '2x', args.outputfile, threads=int( args.threads ) );
            else:
                handler.handler( 'bin/lib/FidelityFX_CLI.exe', args.inputfile, 'custom', '2x', args.outputfile )
