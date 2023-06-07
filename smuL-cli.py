"""
*				FSRSimpleMediaUpscalerLiteFrontend - fsrSimpleMediaUpscalerLite-cli.py
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
import json

engineList = os.listdir( 'bin/engines' );
counter = 0;
for element in engineList: 
    if ( element == '__pycache__' ):
        engineList.pop( counter );
    counter += 1;

engineInfo = {}

for engine in engineList:
    engineInfo[ engine ] = json.load( open( 'bin/engines/' + engine + '/config.json' ) )

allowedFiletypes = [ 'png', 'jpg' ];

def performChecks ( args, ap ):
    if ( args.details == None or args.details == '' ):
        if ( not args.printengines ):
            if ( not args.version ):
                # Check if input and output file arguments are available
                if ( args.inputfile == None or args.inputfile == '' ):
                    print( '\n\n ==> ERROR: Input file required! <==\n\n' )
                    ap.print_usage();
                    return False
                
                output = args.outputfile;
                if ( args.outputfile == None or args.outputfile == '' ):
                    output = args.inputfile[ :len( args.inputfile ) - 4 ] + '_upscaled' + args.inputfile[ len( args.inputfile ) - 4: ]

                # check if output file exists and if, prompt user if it should be overwritten and remove if, if yes
                if ( os.path.exists( output ) ):
                    doReplace = input( '--> File already exists. Do you want to replace it? (Y/n) ' ).lower()
                    if ( doReplace == 'y' or doReplace == '' ):
                        os.remove( output );
                    else:
                        print( '\n==> Refusing to Upscale video. Please delete the file or specify another filepath! <==' )
                        return False
                    
                # check if engine argument is valid
                try:
                    engineInfo[ args.engine.lower() ]
                except KeyError:
                    print( '\n==> ERROR: Engine not available. Ensure you have specified a valid engine' )
                    return False
                
                # Check scalefactor argument and also verify that engine supports upscaling
                if ( args.scalefactor != None and args.scalefactor != 0 ):
                    if ( int( args.scalefactor ) > 4 and int( args.scalefactor ) < -4 ):
                        print( '\n==> ERROR: Invalid scale factor. Value has to be an integer between -4 and 4 (option -s)' )
                        return False
                    else:
                        if ( not 'upscaling' in engineInfo[ args.engine ][ 'supports' ] ):
                            print( '\n==> ERROR: This engine does NOT support upscaling' )
                            return False
                    
                # Check sharpening argument and also verify that engine supports it   
                if ( args.sharpening != None and args.sharpening != 0 ):     
                    if ( float( args.sharpening ) >= 1.0 or float( args.sharpening ) <= 0.0 ):
                        print( '\n==> ERROR: Invalid value for sharpening. Value has to be between 0 and 1' )
                        return False
                    else:
                        if ( not 'sharpening' in engineInfo[ args.engine ][ 'supports' ] ):
                            print( '\n==> ERROR: This engine does NOT support sharpening' )
                            return False
                
                # check if scalefactor and / or sharpening is available
                if ( ( args.scalefactor == 0 or args.scalefactor == None ) and ( args.sharpening == 0 or args.sharpening == None )  ):
                    print( '\n==> ERROR: Either scalefactor or sharpening argument required!' )
                    return False
                
                # Check if filetype argument is valid
                if ( not args.filetype in allowedFiletypes ):
                    print( '\n==> ERROR: Unknown filetype for temp files. Can be png or jpg' )
                    return False
                
                # Check if mode of engine is valid
                if ( args.mode != None ):
                    try:
                        engineInfo[ args.engine.lower() ][ 'cliModeOptions' ][ args.mode.lower() ]
                    except KeyError:
                        print( '\n==> ERROR: The specified mode is not supported by this engine. Options:' )
                        for option in engineInfo[ args.engine ][ 'cliModeOptions' ]:
                            print( '   --> ' + engineInfo[ args.engine ][ 'cliModeOptions' ][ option ][ 'displayName' ] + ' (' + option + ')' )
                        return False
                
                return True
            else:
                print( '\n\n==> You are running Version 1.1.0 of ImageVideoScaler-CLI <==\n' )
        else:
            print( '\n\n==> Available engines <==\n' )
            for entry in engineList:
                print( '--> ' + entry )
            print( '\n\n' )
    else:
        print( '\n\n ==> INFOS about ' + engineInfo[ args.details.lower() ][ 'displayName' ] + '\n' )
        print( '   --> Engine cli option is: ' + engineInfo[ args.details ][ 'abbr' ].lower() )
        print( '   --> CLI mode options are: ' )
        for mode in engineInfo[ args.details ][ 'cliModeOptions' ]:
            print( '       -> ' + engineInfo[ args.details ][ 'cliModeOptions' ][ mode ][ 'displayName' ] + ':' )
            print( '           > CLI name: ' + mode )
            print( '           > Is the default: ' + str( engineInfo[ args.details ][ 'cliModeOptions' ][ mode ][ 'default' ] ) )
        print( '\n\n' )

if __name__ == '__main__':
    ap = argparse.ArgumentParser( description='SimpleMediaUpscalerLite - CLI, a CLI application to upscale videos and images using different upscaling engines.' )
    ap.add_argument( '-i', '--inputfile', help='File path for the video / image to be upscaled' )
    ap.add_argument( '-o', '--outputfile', help='Output file path for the video / image that was upscaled' )
    ap.add_argument( '-s', '--scalefactor', help='Scale factor for the video / image. Can be a integer from -4 to 4' )
    ap.add_argument( '-S', '--sharpening', help='Sharpening factor (between 0 and 1 whereas 0 means no sharpening, 1 the most sharpening. Recommendation: Do not exceed 0.25, as it often looks bad)' )
    ap.add_argument( '-T', '--threads', help='Thread count to use. Cannot exceed CPU thread count. Scaling non-linear (using 2 threads is not exactly 2x the speed of 1 thread). Scales well with FSR, barely with Real-ESRGAN, as it uses mostly the GPU to upscale' )
    ap.add_argument( '-E', '--engine', help='Upscaling engine. By default can be fsr or ss. Use the -p option to see all installed engines' )
    ap.add_argument( '-M', '--mode', help='Specify a special mode for a specific engine. Might not be available in every engine. Use the -d option to find out more' )
    ap.add_argument( '-F', '--filetype', help='Change the file type of the temporary image files. Supports png, jpg. Video quality: png > jpg. PNG is default, if not specified.' )
    ap.add_argument( '-d', '--details', help='Get details on usage of a particular engine and exit. Reads the config.json file of that engine and displays it in a HR manner' )
    ap.add_argument( '-p', '--printengines', help='Print all engines and exit', action='store_true' )
    ap.add_argument( '-v', '--version', help='Print version and exit', action='store_true' )
    ap.set_defaults( scalefactor = 0, sharpening = 0, threads = 4, engine = 'fsr', filetype = 'png' )
    args = ap.parse_args()

    handler = bin.handler.Handler()
    
    multiprocessing.freeze_support();

    if ( performChecks( args, ap ) ):
        output = args.outputfile;
        if ( args.outputfile == None or args.outputfile == '' ):
            output = args.inputfile[ :len( args.inputfile ) - 4 ] + '_upscaled' + args.inputfile[ len( args.inputfile ) - 4: ]

        mode = 'fsr'
        if ( args.mode != None ):
            mode = args.mode
        else:
            for option in engineInfo[ args.engine ][ 'cliModeOptions' ]:
                if ( engineInfo[ args.engine ][ 'cliModeOptions' ][ option ][ 'default' ] ):
                    mode = option
                    break
        if ( handler.handler( args.inputfile, args.scalefactor, output, args.sharpening, args.filetype, args.engine, mode, args.threads ) ):
            print( '\n\n---------------------------------------------------------------------------------\n\nDONE \n\n\n\nSimpleMediaUpscalerLite V1.1.0\n\nCopyright 2023 SimpleMediaUpscalerLite contributors\nThis application comes with absolutely no warranty to the extent permitted by applicable law\n\n\n\nOutput was written to ' + output + '\n\n\n' )
