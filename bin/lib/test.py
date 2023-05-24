import edi
import numpy as np
import argparse

ap = argparse.ArgumentParser( description='Testing for edi. NOTE: No error catching!' )
ap.add_argument( 'inputfile', help='Input file for upscaling' )
ap.add_argument( 'outputfile', help='Output file' )
ap.add_argument( '-S', '--scalefactor', help='Scale factor' )
ap.add_argument( '-a', '--sampling', help='Sampling window size. The bigger, the blurrier. Best >= 4')
ap.set_defaults( sampling=4 )
ap.set_defaults( scalefactor=2 )

args = ap.parse_args()

print( edi.EDI_predict( np.load( args.inputfile, allow_pickle=True ), args.sampling, args.scalefactor ) )