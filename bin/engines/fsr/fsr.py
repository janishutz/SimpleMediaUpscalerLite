import os
import multiprocessing
import time
import subprocess
import sys

class Scaler:
    def __init__( self ):
        self.os_type = sys.platform
        self.command = ''
        self.tmppath = ''
        self.videometa = {}

    def singleScaler ( self, input_path, output_path, scalefactor, threads, mode ):
        if self.os_type == 'linux':
            self.command = f'wine ./bin/lib/FidelityFX_CLI.exe -Mode { mode } -Scale {scalefactor} {scalefactor} {input_path} {output_path}'
        elif self.os_type == 'win32':
            self.command = f'FidelityFX_CLI -Mode { mode } -Scale {scalefactor} {scalefactor} {input_path} {output_path}'
        else:
            print( 'OS CURRENTLY UNSUPPORTED!' )
            return False 
                      
        os.system( self.command )
        print( '\n\n==>Photo upscaled' );

    def videoScaler ( self, tmppath, threads, scalefactor, sharpening, filetype, mode ):
        self.isScaling = True
        if ( scalefactor == 0 or scalefactor == None ):
            self.isScaling = False

        # Locate Images and assemble FSR-Command
        self.file_list = []
        self.filelist = os.listdir( tmppath )
        self.filelist.pop(0)
        self.filelist.sort()
        self.number = 0
        if sharpening != 0 and sharpening != None:
            for self.file in self.filelist:
                self.number += 1
                if ( self.os_type == 'win32' ):
                    self.file_list.append( f"{tmppath}{self.file} {tmppath}up\\up{str(self.number).zfill(8)}.{ filetype } " );
                else:
                    self.file_list.append( f"{tmppath}{self.file} {tmppath}up/up{str(self.number).zfill(8)}.{ filetype } " );
            try:
                os.mkdir( f'{tmppath}up' )
            except FileExistsError:
                pass
        else:
            for self.file in self.filelist:
                self.number += 1
                if ( self.os_type == 'win32' ):
                    self.file_list.append( f"{tmppath}{self.file} {tmppath}sc\\ig{str(self.number).zfill(8)}.{ filetype } " );
                else:
                    self.file_list.append( f"{tmppath}{self.file} {tmppath}sc/ig{str(self.number).zfill(8)}.{ filetype } " );
        
            try:
                os.mkdir( f'{tmppath}sc' )
            except FileExistsError:
                pass
        
        if ( self.os_type == 'win32' ):
            self.maxlength = 8000
        else:
            self.maxlength = 31900
        self.pos = 1

        ############################################
        #
        # Thread optimisation: Divide workload up into different threads & upscale using helper function
        #
        ############################################
        self.threads = threads
        if ( threads > multiprocessing.cpu_count() ):
            self.threads = multiprocessing.cpu_count();

        if ( self.isScaling ):
            engines = { 'c': 'Cubic', 'hqc': 'High Quality Cubic', 'fsr':'FidelityFX Super Resolution' }
            print( f'\n\n==> Upscaling using { self.threads } threads <==\n\n' );
            print( f'\n\n==> Upscaling Engine is FidelityFX_CLI with algorithm { engines[ mode.lower() ] } <==\n\n' );

            time.sleep( 2 );

            self.command_list = [];
            self.file_list_length = len( self.file_list );
            for i in range( self.threads ):
                self.files = '';
                for _ in range( int( self.file_list_length // self.threads ) ):
                    self.files += self.file_list.pop( 0 );
                
                if ( i == self.threads - 1 ):
                    for element in self.file_list:
                        self.files += element;
                self.command_list.append( ( self.files, scalefactor, i, self.maxlength, self.os_type, mode ) )

            self.pool = multiprocessing.Pool( self.threads )
            self.pool.starmap( upscalerEngine, self.command_list );
            self.pool.close();
            self.pool.join();

        if sharpening != 0 and sharpening != None:
            print( f'\n\n\n==> Sharpening using { self.threads } threads <==\n\n' );
            time.sleep( 2 );

            self.pathSharpening = tmppath

            if ( self.isScaling ):
                if ( self.os_type == 'win32' ):
                    self.pathSharpening += 'up\\'
                elif ( self.os_type == 'linux' ):
                    self.pathSharpening += 'up/'

            time.sleep( 2 );
            try:
                os.mkdir( f'{tmppath}sc' )
            except FileExistsError:
                pass
            # Locate Images and assemble FSR-Command
            self.file_list = []
            self.filelist = os.listdir( self.pathSharpening )
            self.filelist.pop(0)
            self.filelist.sort()
            self.number = 0
            for self.file in self.filelist:
                self.number += 1
                if ( self.os_type == 'win32' ):
                    self.file_list.append( f"{self.pathSharpening}{self.file} {tmppath}sc\\ig{str(self.number).zfill(8)}.{ filetype } " );
                else:
                    self.file_list.append( f"{self.pathSharpening}{self.file} {tmppath}sc/ig{str(self.number).zfill(8)}.{ filetype } " );
            
            if ( self.os_type == 'win32' ):
                self.maxlength = 8000
            else:
                self.maxlength = 31900
            self.pos = 1

            # assemble command list
            self.command_list = [];
            self.file_list_length = len( self.file_list );
            for i in range( self.threads ):
                self.files = '';
                for _ in range( int( self.file_list_length // self.threads ) ):
                    self.files += self.file_list.pop( 0 );
                
                if ( i == self.threads - 1 ):
                    for element in self.file_list:
                        self.files += element;
                self.command_list.append( ( self.files, i, self.maxlength, self.os_type, sharpening, not sharpening ) )

            self.pool = multiprocessing.Pool( self.threads )
            self.pool.starmap( sharpeningEngine, self.command_list );
            self.pool.close();
            self.pool.join();

# Add return values

def upscalerEngine ( files, scalefactor, number, maxlength, os_type, version ):
    scaler = 'FSR'
    if ( version.upper() == 'HQC' ):
        scaler = 'HighQualityCubic'
    elif ( version.upper() == 'C' ):
        scaler = 'Cubic'
    files = files;
    # Refactoring of commands that are longer than 32K characters
    fileout = [];
    pos = 0;
    if len( files ) > maxlength:
        while files[maxlength - pos:maxlength - pos + 1] != ' ':
            pos += 1
        file_processing = files[:maxlength - pos]
        if file_processing[len(file_processing) - 14:len(file_processing) - 12] == 'ig':
            pos += 5
        else:
            pass
        while files[maxlength - pos:maxlength - pos + 1] != ' ':
            pos += 1
        fileout.append(files[:maxlength - pos])
        filesopt = files[maxlength - pos:]
        posx = 0
        posy = maxlength

        # Command refactoring for commands that are longer than 64K characters
        if len(filesopt) > maxlength:
            while len(filesopt) > maxlength:
                posx += maxlength - pos
                posy += maxlength - pos
                pos = 1
                while files[posy - pos:posy - pos + 1] != ' ':
                    pos += 1
                file_processing = files[posx:posy - pos]
                if file_processing[len(file_processing) - 14:len(file_processing) - 12] == 'ig':
                    pos += 5
                while files[posy - pos:posy - pos + 1] != ' ':
                    pos += 1

                file_processing = files[posx:posy - pos]
                fileout.append(file_processing)
                filesopt = files[posy - pos:]
            fileout.append(filesopt)
        else:
            fileout.append(files[maxlength - pos:])
    else:
        fileout.append(files)

    # Upscaling images
    print( '\n\n\nUpscaling images... \n\n\n\n\n\n PROCESS: ', number, '\n\n\n' )

    while len( fileout ) > 0:
        files_handle = fileout.pop(0)
        if os_type == 'linux':
            command_us = f'wine ./bin/lib/FidelityFX_CLI.exe -Mode { scaler } -Scale {scalefactor}x {scalefactor}x {files_handle}'
        elif os_type == 'win32':
            command_us = f'FidelityFX_CLI -Mode { scaler } -Scale {scalefactor}x {scalefactor}x {files_handle}'
        else:
            print( 'OS CURRENTLY UNSUPPORTED!' )
            return False
        sub = subprocess.Popen( command_us, shell=True );
        sub.wait();        
        time.sleep(3)
    print( '\n\nCompleted executing Job\n\n\n PROCESS: ', number, '\n\n\n' );


########################
# 
#   Sharpening
#
#######################

def sharpeningEngine ( files, number, maxlength, os_type, sharpening, didUpscale ):
    files = files;
    # Refactoring of commands that are longer than 32K characters
    fileout = [];
    pos = 0;
    if len( files ) > maxlength:
        while files[maxlength - pos:maxlength - pos + 1] != ' ':
            pos += 1
        file_processing = files[:maxlength - pos]
        if ( didUpscale ):
            if file_processing[len(file_processing) - 14:len(file_processing) - 12] == 'up':
                pos += 5
        else:
            if file_processing[len(file_processing) - 17:len(file_processing) - 15] == 'ru':
                pos += 8
        while files[maxlength - pos:maxlength - pos + 1] != ' ':
            pos += 1
        fileout.append(files[:maxlength - pos])
        filesopt = files[maxlength - pos:]
        posx = 0
        posy = maxlength

        # Command refactoring for commands that are longer than 64K characters
        if len(filesopt) > maxlength:
            while len(filesopt) > maxlength:
                posx += maxlength - pos
                posy += maxlength - pos
                pos = 1
                while files[posy - pos:posy - pos + 1] != ' ':
                    pos += 1
                file_processing = files[posx:posy - pos]
                if ( didUpscale ):
                    if file_processing[len(file_processing) - 14:len(file_processing) - 12] == 'up':
                        pos += 5
                else:
                    if file_processing[len(file_processing) - 17:len(file_processing) - 15] == 'ru':
                        pos += 8
                while files[posy - pos:posy - pos + 1] != ' ':
                    pos += 1

                file_processing = files[posx:posy - pos]
                fileout.append(file_processing)
                filesopt = files[posy - pos:]
            fileout.append(filesopt)
        else:
            fileout.append(files[maxlength - pos:])
    else:
        fileout.append(files)

    # Upscaling images
    print( '\n\n\nSharpening images... \n\n\n\n\n\n PROCESS: ', number, '\n\n\n' )

    while len( fileout ) > 0:
        files_handle = fileout.pop(0)
        print( '\n\n\n PROCESS: ', number, '\nRunning sharpening filter\n\n\n' );
        if os_type == 'linux':
            command_sharpening = f'wine ./bin/lib/FidelityFX_CLI.exe -Mode CAS -Sharpness {sharpening} {files_handle}'
        elif os_type == 'win32':
            command_sharpening = f'FidelityFX_CLI -Mode CAS -Sharpness {sharpening} {files_handle}'
        else:
            print( 'OS CURRENTLY UNSUPPORTED!' )
            return False
        sub2 = subprocess.Popen( command_sharpening, shell=True );
        sub2.wait()
        time.sleep(3)
    print( '\n\nCompleted executing Job\n\n\n PROCESS: ', number, '\n\n\n' );

