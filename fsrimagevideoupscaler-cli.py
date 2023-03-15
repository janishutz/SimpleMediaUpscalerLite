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

ap = argparse.ArgumentParser(description="FSRImageVideoUpscaler - CLI")
ap.add_argument("inputfile", help="File path for the video / image to be upscaled")
ap.add_argument("outputfile", help="File path for the video / image that was upscaled")
ap.add_argument('-s', '--scalefactor', help="Scale factor for the video / image")
args = ap.parse_args()

handler = bin.handler.Handler()

if ( args.scalefactor[ len(args.scalefactor) -1:] == 'x' ):
    handler.handler( 'bin/lib/FidelityFX_CLI.exe', args.inputfile, 'custom', args.scalefactor, args.outputfile )
else:
    raise NameError( 'Argument Scale does require to be of form 2x!' )