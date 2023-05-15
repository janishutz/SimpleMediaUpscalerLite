"""
*				FSRImageVideoUpscalerFrontend - handler.py
*
*	Created by Janis Hutz 03/14/2023, Licensed under the GPL V3 License
*			https://janishutz.com, development@janishutz.com
*
*
"""


import os
import sys
import bin.probe
ffmpeg = bin.probe
import configparser
import time
import shutil
import subprocess
import multiprocessing
import itertools


# Loading the config file to get user preferred temp path
config = configparser.ConfigParser()
config.read('./config/settings.ini')


class Handler:
    def __init__(self):
        self.os_type = sys.platform
        self.command = ""
        self.tmppath = ""
        self.videometa = {}


# TODO: CHECK if this upscaler is any good: https://github.com/Maximellerbach/Image-Processing-using-AI (looks quite promising)

    def handler(self, fsrpath, filepath, quality_setting, output_path, sharpening, scaling, filetype, scalerEngine, model, threads=4 ):
        # Function to be called when using this class as this function automatically determines if file is video or image
        print( '\n\nFSRImageVideoUpscalerFrontend - V1.1.0\n\nCopyright 2023 FSRImageVideoUpscalerFrontend contributors\n\n\n\n' );

        if self.os_type == "linux":
            self.tmppath = config["PathSettings"]["tmpPathLinux"]
        elif self.os_type == "win32":
            self.tmppath = config["PathSettings"]["tmpPathWindows"]
        else:
            print("OS CURRENTLY UNSUPPORTED!")
            return False
        if ( self.os_type == 'win32' ):
            self.tmppath += '\\fsru\\'
        else:
            if ( self.tmppath[len(self.tmppath) - 1: ] == '/' ):
                self.tmppath += "fsru/"
            else:
                self.tmppath += '/fsru/'
        # checking for spaces in filepath (for use with terminal commands)
        self.filepath = ""
        for self.letter in filepath:
            if self.letter == " ":
                self.filepath += "\ "
            else:
                self.filepath += self.letter

        # Determining filetype
        if str(filepath)[len(filepath) - 4:] == ".mp4" or str(filepath)[len(filepath) - 4:] == ".mkv" or str(filepath)[len(filepath) - 4:] == ".MP4":
            print( '\n\n==> Upscaling video' )
            self.video_scaling( fsrpath, filepath, quality_setting, output_path, threads, sharpening, scaling, filetype, scalerEngine, model )
        elif str(filepath)[len(filepath) - 4:] == ".JPG" or str(filepath)[len(filepath) - 4:] == ".png" or str(filepath)[len(filepath) - 4:] == ".jpg" or str(filepath)[len(filepath) - 5:] == ".jpeg":
            print( '\n==>upscaling image' )
            self.photo_scaling(fsrpath, filepath, quality_setting, output_path)
        else:
            print("not supported")
            return False

    def photo_scaling(self, fsrpath, filepath, quality_setting, output_path):
        # DO NOT CALL THIS! Use Handler().handler() instead!
        if self.os_type == "linux":
            self.command = f"wine {fsrpath} -Scale {quality_setting} {quality_setting} {self.filepath} {output_path}"
        elif self.os_type == "win32":
            self.command = f"FidelityFX_CLI -Scale {quality_setting} {quality_setting} {self.filepath} {output_path}"
        else:
            print("OS CURRENTLY UNSUPPORTED!")
            return False 
                      
        os.system(self.command)
        print( '\n\n==>Photo upscaled' );

    def video_scaling( self, fsrpath, filepath, quality_setting, output_path, threads, sharpening, scaling, filetype, scalerEngine, model ):
        # DO NOT CALL THIS! Use Handler().handler() instead!
        
        # Splitting video into frames
        try:
            shutil.rmtree(self.tmppath)
        except FileNotFoundError:
            pass
        try:
            os.mkdir(self.tmppath)
        except FileExistsError:
            pass
            
        print( '\n==> Created directory' )
                
        if self.os_type == "linux":
            self.command = f"ffmpeg -i {str(self.filepath)} {self.tmppath}ig%08d.{ filetype }"
        elif self.os_type == "win32":
            self.command = f"ffmpeg -i {str(self.filepath)} \"{self.tmppath}ig%08d.{ filetype }\""
        else:
            print("OS CURRENTLY UNSUPPORTED!")
            return False
        
        os.system( self.command )
        print( '\n==> Video split ' )

        # Retrieving Video metadata
        self.filelist = os.listdir(self.tmppath)
        self.videometa = ffmpeg.probe(str(filepath))["streams"].pop(0)

        self.duration = self.videometa.get( 'duration' )
        self.frames = len( self.filelist )
        try:
            self.framerate = round(float(self.frames) / float(self.duration), 1)
        except TypeError:
            print( '\n\n=> using fallback method to get framerate' )
            self.infos = str( self.videometa.get( 'r_frame_rate' ) )
            self.framerate = float( self.infos[:len(self.infos) - 2] )
            
        print( '\n\n==> Video duration is: ', self.duration, 's' )
        print( '==> Framecount is: ', self.frames, ' frames' )
        print( '==> Frame rate is: ', self.framerate, ' FPS' )
        print( '==> Running with: ', threads, ' threads\n\n' )

        time.sleep( 2 );


        if ( scalerEngine == 'fsr' ):
            self.fsrScaler( self.tmppath, filepath, threads, fsrpath, quality_setting + 'x', sharpening, scaling, filetype )
        elif ( scalerEngine == 'SS' ):
            self.superScaler( self.tmppath, threads, quality_setting, self.os_type, model )
        else:
            raise Exception( 'ERROR upscaling. scalerEngine invalid' );
        
        # get Video's audio
        print( '\n\n==>Finished Upscaling individual images. \n==>Retrieving Video audio to append\n\n' )

        try:
            self.framerate = round(float(self.frames) / float(self.duration), 1)
        except TypeError:
            print( '\n\n=> using fallback method to get framerate' )
            self.infos = str( self.videometa.get( 'r_frame_rate' ) )
            self.framerate = float( self.infos[:len(self.infos) - 2] )

        time.sleep( 2 );
        try:
            os.remove(f"{self.tmppath}audio.aac")
            os.remove(f"{output_path}")
        except FileNotFoundError:
            pass
        if self.os_type == 'linux':
            self.command = f'ffmpeg -i {self.filepath} -vn -acodec copy {self.tmppath}audio.aac'
        elif self.os_type == 'win32':
            self.command = f'ffmpeg -i {self.filepath} -vn -acodec copy {self.tmppath}audio.aac'
        else:
            print( 'OS CURRENTLY UNSUPPORTED!' )
            return False
        os.system( self.command )

        # reassemble Video
        print( '\n\n==>Reassembling Video... with framerate @', self.framerate, '\n\n' )
        if self.os_type == 'linux':
            self.command = f'ffmpeg -framerate {self.framerate} -i {self.tmppath}sc/ig%08d.{filetype} {output_path} -i {self.tmppath}audio.aac'
        elif self.os_type == 'win32':
            self.command = f'ffmpeg -framerate {self.framerate} -i \"{self.tmppath}sc\\ig%08d.{filetype}\" {output_path} -i {self.tmppath}audio.aac'
        else:
            print( 'OS CURRENTLY UNSUPPORTED!' );
            return False
        os.system( self.command )


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


    def fsrScaler ( self, tmppath, filepath, threads, fsrpath, quality_setting, sharpening, scaling, filetype ):
        # Locate Images and assemble FSR-Command
        self.file_list = []
        self.filelist = os.listdir(tmppath)
        self.filelist.pop(0)
        self.filelist.sort()
        self.number = 0
        for self.file in self.filelist:
            self.number += 1
            if ( self.os_type == 'win32' ):
                self.file_list.append( f"{tmppath}{self.file} {tmppath}us\\ig{str(self.number).zfill(8)}.{ filetype } " );
            else:
                self.file_list.append( f"{tmppath}{self.file} {tmppath}us/ig{str(self.number).zfill(8)}.{ filetype } " );
        
        if ( self.os_type == 'win32' ):
            self.maxlength = 8000
        else:
            self.maxlength = 31900
        self.pos = 1

        try:
            os.mkdir( f'{tmppath}us' )
        except FileExistsError:
            pass

        ############################################
        #
        # Thread optimisation: Divide workload up into different threads & upscale using helper function
        #
        ############################################
        self.threads = threads
        if ( threads > multiprocessing.cpu_count() ):
            self.threads = multiprocessing.cpu_count();

        if ( not scaling ):
            print( f'\n\n==> Upscaling using { self.threads } threads <==\n\n' );

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
                self.command_list.append( ( self.files, fsrpath, quality_setting, i, self.maxlength, self.os_type ) )

            self.pool = multiprocessing.Pool( self.threads )
            self.pool.starmap( upscalerEngine, self.command_list );
            self.pool.close();
            self.pool.join();

        if sharpening != '':
            print( f'\n\n\n==> Sharpening using { self.threads } threads <==\n\n' );
            time.sleep( 2 );

            self.pathSharpening = tmppath

            if ( not scaling ):
                self.pathSharpening += 'us'

            time.sleep( 2 );
            try:
                os.mkdir( f'{tmppath}sh' )
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
                    self.file_list.append( f"{self.pathSharpening}\\{self.file} {tmppath}sh\\ig{str(self.number).zfill(8)}.{ filetype } " );
                else:
                    self.file_list.append( f"{self.pathSharpening}/{self.file} {tmppath}sh/ig{str(self.number).zfill(8)}.{ filetype } " );
            
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
                self.command_list.append( ( self.files, fsrpath, i, self.maxlength, self.os_type, sharpening ) )

            self.pool = multiprocessing.Pool( self.threads )
            self.pool.starmap( sharpeningEngine, self.command_list );
            self.pool.close();
            self.pool.join();



def upscalerEngine ( files, fsrpath, quality_setting, number, maxlength, os_type ):
    files = files;
    # Refactoring of commands that are longer than 32K characters
    fileout = [];
    pos = 0;
    if len( files ) > maxlength:
        while files[maxlength - pos:maxlength - pos + 1] != ' ':
            pos += 1
        file_processing = files[:maxlength - pos]
        if file_processing[len(file_processing) - 14:len(file_processing) - 12] == 'ex':
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
                if file_processing[len(file_processing) - 14:len(file_processing) - 12] == 'ex':
                    pos += 5
                else:
                    pass
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
            command_us = f'wine {fsrpath} -Scale {quality_setting} {quality_setting} {files_handle}'
        elif os_type == 'win32':
            command_us = f'FidelityFX_CLI -Scale {quality_setting} {quality_setting} {files_handle}'
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

def sharpeningEngine ( files, fsrpath, number, maxlength, os_type, sharpening ):
    files = files;
    # Refactoring of commands that are longer than 32K characters
    fileout = [];
    pos = 0;
    if len( files ) > maxlength:
        while files[maxlength - pos:maxlength - pos + 1] != ' ':
            pos += 1
        file_processing = files[:maxlength - pos]
        if file_processing[len(file_processing) - 14:len(file_processing) - 12] == 'ex':
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
                if file_processing[len(file_processing) - 14:len(file_processing) - 12] == 'ex':
                    pos += 5
                else:
                    pass
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
            command_sharpening = f'wine {fsrpath} -Mode CAS -Sharpness {sharpening} {files_handle}'
        elif os_type == 'win32':
            command_sharpening = f'FidelityFX_CLI -Mode CAS -Sharpness {sharpening} {files_handle}'
        else:
            print( 'OS CURRENTLY UNSUPPORTED!' )
            return False
        sub2 = subprocess.Popen( command_sharpening, shell=True );
        sub2.wait()
        time.sleep(3)
    print( '\n\nCompleted executing Job\n\n\n PROCESS: ', number, '\n\n\n' );

