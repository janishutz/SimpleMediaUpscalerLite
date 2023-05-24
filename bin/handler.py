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
import bin.engines.ss
import bin.engines.fsr

fsr = bin.engines.fsr.FSRScaler()
ss = bin.engines.ss.SpecialScaler()


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

    def handler(self, fsrpath, filepath, quality_setting, output_path, sharpening, scaling, filetype, scalerEngine, model, useSpecialModeSS, threads=4 ):
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
            self.video_scaling( fsrpath, filepath, quality_setting, output_path, threads, sharpening, scaling, filetype, scalerEngine, model, useSpecialModeSS )
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

    def video_scaling( self, fsrpath, filepath, quality_setting, output_path, threads, sharpening, scaling, filetype, scalerEngine, model, useSpecialModeSS ):
        # DO NOT CALL THIS! Use Handler().handler() instead!
        
        # Splitting video into frames
        try:
            shutil.rmtree(self.tmppath)
        except FileNotFoundError:
            pass
        try:
            os.mkdir(self.tmppath)
        except FileExistsError:
            print( '==> ERROR: Temp path does not exist! <==' )
            return False
            
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

        self.lastUsedPath = ''

        if ( scalerEngine.lower() == 'fsr' or scalerEngine.lower() == 'c' or scalerEngine.lower() == 'hqc' ):
            self.lastUsedPath = fsr.fsrScaler( self.tmppath, filepath, threads, fsrpath, quality_setting + 'x', sharpening, scaling, filetype, scalerEngine )
        elif ( scalerEngine.upper() == 'SS' ):
            if ( not useSpecialModeSS ):
                self.lastUsedPath = ss.superScaler( self.tmppath, threads, quality_setting, self.os_type, model )
            else:   
                self.lastUsedPath = ss.specialSuperScaler( self.tmppath, threads, quality_setting, model )
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
        print( '\n\n==> Reassembling Video... with framerate @', self.framerate, '\n\n' )
        if self.os_type == 'linux':
            self.command = f'ffmpeg -framerate {self.framerate} -i {self.tmppath}sc/ig%08d.{filetype} {output_path} -i {self.tmppath}audio.aac'
        elif self.os_type == 'win32':
            self.command = f'ffmpeg -framerate {self.framerate} -i \"{self.tmppath}sc\\ig%08d.{filetype}\" {output_path} -i {self.tmppath}audio.aac'
        else:
            print( 'OS CURRENTLY UNSUPPORTED!' );
            return False
        os.system( self.command )