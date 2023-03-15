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
ap.add_argument("Input file", help="Path to txt file containing the testdata")
args = ap.parse_args()

handler = bin.handler.Handler()

handler.handler( 'bin/lib/FidelityFX_CLI.exe',  )