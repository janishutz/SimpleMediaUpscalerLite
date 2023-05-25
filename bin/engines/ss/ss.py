import os
import subprocess
import multiprocessing
import time
import sys

class Scaler:
    def __init__(self):
        self.os_type = sys.platform
        self.command = ""
        self.tmppath = ""
        self.videometa = {}

    def singleScaler ( self, input_path, output_path, scalefactor, threads, mode ):
        if self.os_type == 'linux':
            self.command = f'wine ./bin/lib/FidelityFX_CLI.exe -Scale {scalefactor} {scalefactor} {input_path} {output_path} -n { mode }'
        elif self.os_type == 'win32':
            self.command = f'realesrgan-ncnn-vulkan -i {input_path} -o {output_path} -s {scalefactor} -j {threads}:{threads}:{threads} -n { mode }'
        else:
            print( 'OS CURRENTLY UNSUPPORTED!' )
            return False 
                      
        os.system( self.command )
        print( '\n\n==>Photo upscaled' );

    def videoScaler ( self, tmppath, threads, scalefactor, sharpening, filetype, mode ):
        modes = { 'av3':'realesr-animevideov3', 'x4plus': 'realesrgan-x4plus-anime' }
        print( '\n\n==> Preparing to upscale videos <==\n\n==> You will see a lot of numbers flying by showing the progress of the upscaling of each individual image.\n==> This process might take a long time, depending on the length of the video.\n\n')
        time.sleep( 2 );

        try:
            os.mkdir( f'{tmppath}sc' )
        except FileExistsError:
            pass
        if ( self.os_type == 'win32' ):
            self.command = f'realesrgan-ncnn-vulkan -i {tmppath} -o {tmppath}sc -s {scalefactor} -j {threads}:{threads}:{threads} -n {modes[ mode ]}'
        elif ( self.os_type == 'linux' ):
            self.command = f'wine ./bin/lib/realesrgan-ncnn-vulkan.exe -i {tmppath} -o {tmppath}sc -s {scalefactor} -j {threads}:{threads}:{threads} -n {modes[ mode ]}'
        os.system( self.command );