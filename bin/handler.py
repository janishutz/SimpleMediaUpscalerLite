'''
*				FSRSimpleMediaScalerLiteFrontend - handler.py
*
*	Created by Janis Hutz 03/14/2023, Licensed under the GPL V3 License
*			https://janishutz.com, development@janishutz.com
*
*
'''


import os
import sys
import bin.probe
ffmpeg = bin.probe
import configparser
import json
import importlib
import shutil
import time

importedModules = {}

engineList = os.listdir( 'bin/engines' );
engineList.pop( 0 )

for element in engineList:
    importedModules[ element ] = importlib.import_module( 'bin.engines.' + element + '.' + element ).Scaler()

# Loading the config file to get user preferred temp path
config = configparser.ConfigParser()
config.read('./config/settings.ini')


class Handler:
    def __init__(self):
        self.os_type = sys.platform
        self.command = ''
        self.tmppath = ''
        self.videometa = {}


# TODO: CHECK if this upscaler is any good: https://github.com/Maximellerbach/Image-Processing-using-AI (looks quite promising)

    def handler( self, filepath, scalefactor, output_path, sharpening, filetype, engine, mode, threads=4 ):
        # Function to be called when using this class as this function automatically determines if file is video or image
        print( '\n\n SimpleMediaScalerLite - V1.1.0\n\n(c) 2023 SimpleMediaScalerLite contributors\n\n\n\n' );

        if self.os_type == 'linux':
            self.tmppath = config['PathSettings']['tmpPathLinux']
        elif self.os_type == 'win32':
            self.tmppath = config['PathSettings']['tmpPathWindows']
        else:
            print('OS CURRENTLY UNSUPPORTED!')
            return False
        if ( self.os_type == 'win32' ):
            self.tmppath += '\\fsru\\'
        else:
            if ( self.tmppath[len(self.tmppath) - 1: ] == '/' ):
                self.tmppath += 'fsru/'
            else:
                self.tmppath += '/fsru/'

        # checking for spaces in filepath (for use with terminal commands)
        self.filepath = ''
        for self.letter in filepath:
            if self.letter == ' ':
                self.filepath += '\ '
            else:
                self.filepath += self.letter
            
        try:
            shutil.rmtree(self.tmppath)
        except FileNotFoundError:
            pass
        try:
            os.mkdir(self.tmppath)
        except FileExistsError:
            print( '==> ERROR: Temp path does not exist! <==' )
            return False

        # Determining filetype
        if str(filepath)[len(filepath) - 4:] == '.mp4' or str(filepath)[len(filepath) - 4:] == '.mkv' or str(filepath)[len(filepath) - 4:] == '.MP4':
            print( '\n\n==> Upscaling video' )
            self.video_scaling( filepath, output_path, scalefactor, threads, sharpening, filetype, mode, engine )
        elif str(filepath)[len(filepath) - 4:] == '.JPG' or str(filepath)[len(filepath) - 4:] == '.png' or str(filepath)[len(filepath) - 4:] == '.jpg' or str(filepath)[len(filepath) - 5:] == '.jpeg':
            print( '\n==> Upscaling Image' )
            self.photo_scaling( filepath, output_path, scalefactor, sharpening, threads, engine, mode )
        else:
            print('not supported')
            return False

    def photo_scaling(self, input_path, output_path, scalefactor, sharpening, threads, engine, mode ):
        # DO NOT CALL THIS! Use Handler().handler() instead!
        importedModules[ engine ].singleScaler( input_path, output_path, scalefactor, sharpening, threads, mode, self.tmppath );

    def video_scaling( self, input_path, output_path, scalefactor, threads, sharpening, filetype, mode, engine ):
        self.engineSetting = json.load( open( 'bin/engines/' + engine + '/config.json' ) )
        # DO NOT CALL THIS! Use Handler().handler() instead!
        
        # Splitting video into frames
            
        print( '\n==> Created directory' )
                
        if self.os_type == 'linux':
            self.command = f'ffmpeg -i {str(self.filepath)} {self.tmppath}ig%08d.{ filetype }'
        elif self.os_type == 'win32':
            self.command = f'ffmpeg -i {str(self.filepath)} \"{self.tmppath}ig%08d.{ filetype }\"'
        else:
            print('OS CURRENTLY UNSUPPORTED!')
            return False
        
        os.system( self.command )
        print( '\n==> Video split ' )

        # Retrieving Video metadata
        self.filelist = os.listdir(self.tmppath)
        self.videometa = ffmpeg.probe(str(input_path))['streams'].pop(0)

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

        importedModules[ engine ].videoScaler ( self.tmppath, int( threads ), int( scalefactor ), float( sharpening ), filetype, mode )
        
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
            os.remove(f'{self.tmppath}audio.aac')
            os.remove(f'{output_path}')
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
            self.command = f'ffmpeg -framerate {self.framerate} -i {self.tmppath}{self.engineSetting[ "lastUsedFilePath" ]}/{self.engineSetting[ "fileNameBeginning" ]}%08d.{filetype} {output_path} -i {self.tmppath}audio.aac'
        elif self.os_type == 'win32':
            self.command = f'ffmpeg -framerate {self.framerate} -i \'{self.tmppath}{self.engineSetting[ "lastUsedFilePath" ]}\\{self.engineSetting[ "fileNameBeginning" ]}%08d.{filetype}\' {output_path} -i {self.tmppath}audio.aac'
        else:
            print( 'OS CURRENTLY UNSUPPORTED!' );
            return False
        os.system( self.command )