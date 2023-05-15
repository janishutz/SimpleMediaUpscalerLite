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

allowedFiletypes = [ 'png', 'jpg' ];

if __name__ == '__main__':
    ap = argparse.ArgumentParser( description='FSRImageVideoUpscaler - CLI, a CLI application to upscale videos and images using FSR.' )
    ap.add_argument( 'inputfile', help='File path for the video / image to be upscaled' )
    ap.add_argument( 'outputfile', help='File path for the video / image that was upscaled' )
    ap.add_argument( '-s', '--scalefactor', help='Scale factor for the video / image. Can be a integer from 1 - 4' )
    ap.add_argument( '-F', '--filetype', help='Change the file type of the temporary image files. Supports png, jpg. Video quality: png > jpg. Png is default, if not specified.' )
    ap.add_argument( '-S', '--sharpening', help='Sharpening factor (between 0 and 1 whereas 0 means no sharpening, 1 the most sharpening. Recommendation: Do not exceed 0.25, as it often looks bad)' )
    ap.add_argument( '-N', '--noscaling', help='Do not upscale video, instead only sharpen. Sharpening argument required!', action='store_true' )
    ap.add_argument( '-T', '--threads', help='Thread count to use. Cannot exceed CPU thread count. Scaling non-linear (using 2 threads is not exactly 2x the speed of 1 thread). Scales well with FSR, barely with Real-ESRGAN, as it uses mostly the GPU to upscale' )
    ap.add_argument( '-E', '--engine', help='Upscaling engine. Can be fsr or SS (for Real-ESRGAN). FSR tends to be lower quality, but faster, Real-ESRGAN is meant for anime. Defaults to fsr' )
    ap.add_argument( '-M', '--model', help='Only available if using Real-ESRGAN. Change the ML-Model used to upsample video, can be: realesr-animevideov3 | realesrgan-x4plus-anime , defaults to realesr-animevideov3' )
    args = ap.parse_args()

    handler = bin.handler.Handler()

    go = True;
    go2 = True;
    go3 = True;
    engine = 'fsr';
    model = 'realesr-animevideov3';
    availableModels = [ 'realesr-animevideov3', 'realesrgan-x4plus-anime' ];

    multiprocessing.freeze_support();
    if ( os.path.exists( args.outputfile ) ):
        doReplace = input( 'File already exists. Do you want to replace it? (Y/n) ' ).lower()
        if ( doReplace == 'y' or doReplace == '' ):
            go = True
            os.remove( args.outputfile );
        else:
            print( '\nRefusing to Upscale video. Please delete the file or specify another filepath!')
            go = False

    if ( args.engine != None ):
        if ( args.engine == 'fsr' or args.engine == 'SS' ):
            engine = args.engine;
        else:
            print( 'Invalid argument for engine' )
            go2 = False;
    
    if ( engine == 'SS' and args.model != None ):
        if ( args.model in availableModels ):
            model = args.model;
        else:
            print( 'Invalid argument for model. Can be: realesr-animevideov3 | realesrgan-x4plus | realesrgan-x4plus-anime | realesrnet-x4plus' )
            go2 = False;

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
            print( 'Invalid filetype for temp images specified. Please ensure to only use png or jpg!' );
    else:
        filetype = 'png'


    if ( go and go2 and go3 ):
        if ( args.scalefactor ):
            if ( int( args.scalefactor ) ):
                if ( args.threads != None ):
                    handler.handler( 'bin/lib/FidelityFX_CLI.exe', args.inputfile, args.scalefactor, args.outputfile, args.sharpening, args.noscaling, filetype, engine, model, threads=int( args.threads ) );
                else:
                    handler.handler( 'bin/lib/FidelityFX_CLI.exe', args.inputfile, args.scalefactor, args.outputfile, args.sharpening, args.noscaling, filetype, engine, model );
            else:
                raise NameError( 'Argument Scale does require to be an integer!' )
        else:
            if ( args.threads != None ):
                handler.handler( 'bin/lib/FidelityFX_CLI.exe', args.inputfile, '2', args.outputfile, args.sharpening, args.noscaling, filetype, engine, model, threads=int( args.threads ) );
            else:
                handler.handler( 'bin/lib/FidelityFX_CLI.exe', args.inputfile, '2', args.outputfile, args.sharpening, args.noscaling, filetype, engine, model )
        print( '\n\n---------------------------------------------------------------------------------\n\nDONE \n\n\n\nImageVideoUpscalerFrontend V1.1.0\n\nCopyright 2023 FSRImageVideoUpscalerFrontend contributors\nThis application comes with absolutely no warranty to the extent permitted by applicable law\n\n\n\nYour video was saved to ' + args.outputfile + '\n\n\n' )

