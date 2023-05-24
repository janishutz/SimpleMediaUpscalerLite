import os
import subprocess
import multiprocessing
import time
import sys

class SpecialScaler:
    def __init__(self):
        self.os_type = sys.platform
        self.command = ""
        self.tmppath = ""
        self.videometa = {}

    def superScaler ( self, tmppath, threads, quality_setting, os_platform, model ):
        print( '\n\n==> Preparing to upscale videos <==\n\n==> You will see a lot of numbers flying by showing the progress of the upscaling of each individual image.\n==> This process might take a long time, depending on the length of the video.\n\n')
        time.sleep( 2 );

        try:
            os.mkdir( f'{tmppath}sc' )
        except FileExistsError:
            pass
        if ( os_platform == 'win32' ):
            self.command = f'realesrgan-ncnn-vulkan -i {tmppath} -o {tmppath}sc -s {quality_setting} -j {threads}:{threads}:{threads} -n {model}'
        elif ( os_platform == 'linux' ):
            self.command = f'wine ./bin/lib/realesrgan-ncnn-vulkan.exe -i {tmppath} -o {tmppath}sc -s {quality_setting} -j {threads}:{threads}:{threads} -n {model}'
        os.system( self.command );


    def specialSuperScaler ( self, tmppath, threads, quality_setting, model ):
        self.fileList = os.listdir( tmppath )
        self.fileList.pop( 0 )
        self.fileList.sort()
        if ( threads > multiprocessing.cpu_count() * 2 ):
            self.threads = multiprocessing.cpu_count() * 2;
        else:
            self.threads = threads
    
        self.fileCount = len( self.fileList ) // self.threads
        self.spareFiles = len( self.fileList ) % self.threads
        
        self.cmdList = [];

        for t in range( threads ): 
            try:
                os.mkdir( f'{tmppath}{t}' )
            except FileExistsError:
                pass

            self.base = t * self.fileCount;
            if ( self.os_type == 'win32' ):
                for j in range( self.fileCount ):
                    os.rename( f'{tmppath}{self.fileList[ self.base + j ] }', f'{tmppath}{ t }\\{self.fileList[ self.base + j ] }' )
            elif ( self.os_type == 'linux' ):
                for j in range( self.fileCount ):
                    os.rename( f'{tmppath}{self.fileList[ self.base + j ] }', f'{tmppath}{ t }/{self.fileList[ self.base + j ] }' )
            
            self.cmdList.append( ( tmppath, t, quality_setting, model, self.os_type ) )

        try:
            os.mkdir( f'{tmppath}{self.threads + 1}' )
        except FileExistsError:
            pass

        if ( self.os_type == 'win32' ):
            for k in range( self.spareFiles ):
                os.rename( f'{tmppath}{self.fileList[ self.threads * self.fileCount + k ] }', f'{tmppath}{ t }\\{self.fileList[ self.threads  * self.fileCount + k ] }' )
        elif ( self.os_type == 'linux' ):
            for k in range( self.spareFiles ):
                os.rename( f'{tmppath}{self.fileList[ self.threads * self.fileCount + k ] }', f'{tmppath}{ self.threads + 1 }/{self.fileList[ self.threads * self.fileCount + k ] }' )

        try:
            os.mkdir( f'{tmppath}sc' )
        except FileExistsError:
            pass

        self.pool_ss = multiprocessing.Pool( self.threads )
        self.pool_ss.starmap( specialScalerEngine, self.cmdList );
        self.pool_ss.close();
        self.pool_ss.join();
    
        specialScalerEngine( tmppath, t, quality_setting, model, self.os_type )


def specialScalerEngine ( tmppath, tNumber, quality_setting, model, os_type ):
    if ( os_type == 'win32' ):
        command = f'realesrgan-ncnn-vulkan -i {tmppath}{tNumber} -o {tmppath}sc -s {quality_setting} -n {model}'
    elif ( os_type == 'linux' ):
        command = f'wine ./bin/lib/realesrgan-ncnn-vulkan.exe -i {tmppath}{tNumber} -o {tmppath}sc -s {quality_setting} -n {model}'
    sub = subprocess.Popen( command, shell=True );
    sub.wait();