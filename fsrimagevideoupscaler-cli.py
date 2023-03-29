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

allowedFiletypes = [ 'bmp', 'png', 'jpg' ];

if __name__ == '__main__':
    ap = argparse.ArgumentParser( description='FSRImageVideoUpscaler - CLI, a CLI application to upscale videos and images using FSR.' )
    ap.add_argument( 'inputfile', help='File path for the video / image to be upscaled' )
    ap.add_argument( 'outputfile', help='File path for the video / image that was upscaled' )
    ap.add_argument( '-s', '--scalefactor', help='Scale factor for the video / image' )
    ap.add_argument( '-F', '--filetype', help='Change the file type of the temporary image files. Supports bmp, png, jpg. Video quality: bmp > png > jpg. Only use bmp for short videos only, or on high end, high-capacity SSDs, as it uses lots of storage space! png is default, if not specified.' )
    ap.add_argument( '-S', '--sharpening', help='Sharpening factor (between 0 and 1 wheras 0 means no sharpening, 1 the most sharpening. Recommendation: Do not exceed 0.25, as it often looks bad)' )
    ap.add_argument( '-N', '--noscaling', help='Do not upscale video, instead only sharpen. Sharpening argument required!', action='store_true' )
    ap.add_argument( '-T', '--threads', help='Thread count to use. Cannot exceed CPU thread count. Scaling non-linear (using 2 threads is not exactly 2x the speed of 1 thread)' )
    args = ap.parse_args()

    handler = bin.handler.Handler()

    go = True;
    go2 = True;
    go3 = True;

    multiprocessing.freeze_support();
    if ( os.path.exists( args.outputfile ) ):
        if ( input( 'File already exists. Do you want to replace it? (y/n) ' ).lower() == 'y' ):
            go = True
            os.remove( args.outputfile );
        else:
            print( '\nRefusing to Upscale video. Please delete the file or specify another filepath!')
            go = False

    if ( args.noscaling ):
        if ( args.sharpening != None ):
            if ( float( args.sharpening ) > 0 ):
                go2 = True;
            else: 
                go2 = False;
        else:
            print( 'Missing argument for Sharpening. Please specify that argument and try again!' )
            go2 = False;

    if ( args.sharpening != None ):
        if ( float( args.sharpening ) > 1 ):
            print( 'Invalid argument for Sharpening, please specify  value between 0 and 1!' )
            go3 = False;
    
    if ( args.filetype != None ):
        if ( args.filetype in allowedFiletypes ):
            filetype = args.filetype
        else:
            g3o = False
            print( 'Invalid filetype for temp images specified. Please ensure to only use png, bmp or jpg!' );
    else:
        filetype = 'png'


    if ( go and go2 and go3 ):
        if ( args.scalefactor ):
            if ( args.scalefactor[ len(args.scalefactor) -1: ] == 'x' ):
                if ( args.threads != None ):
                    handler.handler( 'bin/lib/FidelityFX_CLI.exe', args.inputfile, 'custom', args.scalefactor, args.outputfile, args.sharpening, args.noscaling, filetype, threads=int( args.threads ) );
                else:
                    handler.handler( 'bin/lib/FidelityFX_CLI.exe', args.inputfile, 'custom', args.scalefactor, args.outputfile, args.sharpening, args.noscaling, filetype );
            else:
                raise NameError( 'Argument Scale does require to be of form 2x! (it has to end in x)' )
        else:
            if ( args.threads != None ):
                handler.handler( 'bin/lib/FidelityFX_CLI.exe', args.inputfile, 'custom', '2x', args.outputfile, args.sharpening, args.noscaling, filetype, threads=int( args.threads ) );
            else:
                handler.handler( 'bin/lib/FidelityFX_CLI.exe', args.inputfile, 'custom', '2x', args.outputfile, args.sharpening, args.noscaling, filetype )
        print( '\n\n---------------------------------------------------------------------------------\n\nDONE \n\nFSRImageVideoUpscalerFrontend V1.1.0\n\nCopyright 2023 FSRImageVideoUpscalerFrontend contributors\nThis application comes with absolutely no warranty to the extent permitted by applicable law\n\n' )

