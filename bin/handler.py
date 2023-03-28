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

    def handler(self, fsrpath, filepath, quality_mode, quality_setting, output_path, threads=4):
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
            self.video_scaling(fsrpath, filepath, quality_mode, quality_setting, output_path, threads)
        elif str(filepath)[len(filepath) - 4:] == ".JPG" or str(filepath)[len(filepath) - 4:] == ".png" or str(filepath)[len(filepath) - 4:] == ".jpg" or str(filepath)[len(filepath) - 5:] == ".jpeg":
            print( '\n==>upscaling image' )
            self.photo_scaling(fsrpath, filepath, quality_mode, quality_setting, output_path)
        else:
            print("not supported")
            return False

    def photo_scaling(self, fsrpath, filepath, quality_mode, quality_setting, output_path):
        # DO NOT CALL THIS! Use Handler().handler() instead!
        if quality_mode == "default":
            if self.os_type == "linux":
                self.command = f"wine {fsrpath} -QualityMode {quality_setting} {self.filepath} {output_path}"
            elif self.os_type == "win32":
                self.command = f"FidelityFX_CLI -QualityMode {quality_setting} {self.filepath} {output_path}"
            else:
                print("OS CURRENTLY UNSUPPORTED!")
                return False
        else:
            if self.os_type == "linux":
                self.command = f"wine {fsrpath} -Scale {quality_setting} {quality_setting} {self.filepath} {output_path}"
            elif self.os_type == "win32":
                self.command = f"FidelityFX_CLI -Scale {quality_setting} {quality_setting} {self.filepath} {output_path}"
            else:
                print("OS CURRENTLY UNSUPPORTED!")
                return False 
                      
        os.system(self.command)
        print( '\n\n==>Photo upscaled' );

    def video_scaling(self, fsrpath, filepath, quality_mode, quality_setting, output_path, threads):
        # DO NOT CALL THIS! Use Handler().handler() instead!
        self.videometa = ffmpeg.probe(str(filepath))["streams"].pop(0)

        # Retrieving Video metadata
        self.duration = self.videometa.get( 'duration' )
        self.frames = self.videometa.get( 'nb_frames' )
        try:
            self.framerate = round(float(self.frames) / float(self.duration), 1)
        except TypeError:
            self.infos = str( self.videometa.get("r_frame_rate") )
            print( '\n\n=> using fallback method to get framerate' )
            self.framerate = float(self.infos[:len(self.infos) - 2])
            
        print( '==> Video duration is: ', self.duration, 's' )
        print( '==> Framecount is: ', self.frames, ' frames' )
        print( '==> Frame rate is: ', self.framerate, ' FPS' )
        print( '==> Running with ', threads, ' threads\n\n' )

        time.sleep( 2 );

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
            self.command = f"ffmpeg -i {str(self.filepath)} {self.tmppath}ex%08d.png"
        elif self.os_type == "win32":
            self.command = f"ffmpeg -i {str(self.filepath)} \"{self.tmppath}ex%08d.png\""
        else:
            print("OS CURRENTLY UNSUPPORTED!")
            return False
        
        os.system( self.command )
        print( '\n==> Video split ' )

        # Locate Images and assemble FSR-Command
        self.file_list = []
        self.filelist = os.listdir(self.tmppath)
        self.filelist.pop(0)
        self.filelist.sort()
        self.number = 0
        for self.file in self.filelist:
            self.number += 1
            if ( self.os_type == 'win32' ):
                self.file_list.append( f"{self.tmppath}{self.file} {self.tmppath}sc\\ig{str(self.number).zfill(8)}.png " );
            else:
                self.file_list.append( f"{self.tmppath}{self.file} {self.tmppath}sc/ig{str(self.number).zfill(8)}.png " );
        
        if ( self.os_type == 'win32' ):
            self.maxlength = 8000
        else:
        	self.maxlength = 31900
        self.pos = 1

        try:
            os.mkdir(f"{self.tmppath}sc")
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

        print( f'\n\n==>Using { self.threads } threads <==\n\n' );

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
            self.command_list.append( ( quality_mode, self.files, fsrpath, quality_setting, i, self.maxlength, self.os_type ) )

        self.pool = multiprocessing.Pool( self.threads )
        self.pool.starmap( upscalerEngine, self.command_list );
        self.pool.close();
        self.pool.join();

        
        # get Video's audio
        print( '\n\n==>Finished Upscaling individual images. \n==>Retrieving Video audio to append\n\n' )
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
            self.command = f'ffmpeg -framerate {self.framerate} -i {self.tmppath}sc/ig%08d.png {output_path} -i {self.tmppath}audio.aac'
        elif self.os_type == 'win32':
            self.command = f'ffmpeg -framerate {self.framerate} -i \"{self.tmppath}sc\\ig%08d.png\" {output_path} -i {self.tmppath}audio.aac'
        else:
            print( 'OS CURRENTLY UNSUPPORTED!' );
            return False
        os.system( self.command )

        print( '\n\n---------------------------------------------------------------------------------\n\nDONE \n\nFSRImageVideoUpscalerFrontend V1.1.0\n\nCopyright 2023 FSRImageVideoUpscalerFrontend contributors\nThis application comes with absolutely no warranty to the extent permitted by applicable law\n\n' )


def upscalerEngine (  quality_mode, files, fsrpath, quality_setting, number, maxlength, os_type ):
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
        if quality_mode == 'default':
            if os_type == 'linux':
                command_us = f'wine {fsrpath} -QualityMode {quality_setting} {files_handle}'
            elif os_type == 'win32':
                command_us = f'FidelityFX_CLI -QualityMode {quality_setting} {files_handle}'
            else:
                print( 'OS CURRENTLY UNSUPPORTED!' )
                return False
        else:
            if os_type == "linux":
                command_us = f'wine {fsrpath} -Scale {quality_setting} {quality_setting} {files_handle}'
            elif os_type == "win32":
                command_us = f'FidelityFX_CLI -Scale {quality_setting} {quality_setting} {files_handle}'
            else:
                print( 'OS CURRENTLY UNSUPPORTED!' )
                return False
        sub = subprocess.Popen( command_us, shell=True );
        sub.wait();
        time.sleep(3)
    print( '\n\nCompleted executing Job\n\n\n PROCESS: ', number, '\n\n\n' );
