###########################################################
#
# Handler for FSRImageVideoUpscalerFrontend
#
# This code is licensed under the GPL V3 License!
# Developed 2022 by Janis Hutz
#
###########################################################

import os
import sys
import ffmpeg
import configparser

# Loading the config file to get user preferred temp path
config = configparser.ConfigParser()
config.read('../config/settings.ini')


class Handler:
    def __init__(self):
        self.os_type = sys.platform
        self.command = ""
        self.tmppath = ""
        self.videometa = {}

    def handler(self, fsrpath, filepath, quality_mode, quality_setting, output_path, ffmpegpath):
        # Function to be called when using this class as this function automatically determines if file is video or image
        if self.os_type == "linux":
            self.tmppath = "/tmp/fsru/" # config["PathSettings"]["tmpPathLinux"]
        elif self.os_type == "win32":
            self.tmppath = config["PathSettings"]["tmpPathWindows"]
        else:
            print("OS CURRENTLY UNSUPPORTED!")
            return False
        # checking for spaces in filepath (for use with terminal commands)
        self.filepath = ""
        for self.letter in filepath:
            if self.letter == " ":
                self.filepath += "\ "
            else:
                self.filepath += self.letter

        # Determining filetype
        if str(filepath)[len(filepath) - 4:] == ".mp4" or str(filepath)[len(filepath) - 4:] == ".mkv":
            print("upscaling video")
            self.video_scaling(ffmpegpath, fsrpath, filepath, quality_mode, quality_setting, output_path)
        elif str(filepath)[len(filepath) - 4:] == ".JPG" or str(filepath)[len(filepath) - 4:] == ".png" or str(filepath)[len(filepath) - 4:] == ".jpg":
            print("upscaling image")
            self.photo_scaling(fsrpath, filepath, quality_mode, quality_setting, output_path)
        else:
            print("not supported")

    def photo_scaling(self, fsrpath, filepath, quality_mode, quality_setting, output_path):
        # DO NOT CALL THIS! Use Handler().handler() instead!
        if quality_mode == "default":
            if self.os_type == "linux":
                self.command = f"wine {fsrpath} -QualityMode {quality_setting} {self.filepath} {output_path}"
            elif self.os_type == "win32":
                self.command = f"{fsrpath} -QualityMode {quality_setting} {self.filepath} {output_path}"
            else:
                print("OS CURRENTLY UNSUPPORTED!")
                return False

            os.system(self.command)
            print("photo upscaled")
        else:
            if self.os_type == "linux":
                self.command = f"wine {fsrpath} -Scale {quality_setting} {self.filepath} {output_path}"
            elif self.os_type == "win32":
                self.command = f"{fsrpath} -Scale {quality_setting} {self.filepath} {output_path}"
            else:
                print("OS CURRENTLY UNSUPPORTED!")
                return False
            os.system(self.command)
            print("photo upscaled")

    def video_scaling(self, ffmpegpath, fsrpath, filepath, quality_mode, quality_setting, output_path):
        # DO NOT CALL THIS! Use Handler().handler() instead!
        self.videometa = ffmpeg.probe(str(filepath))["streams"].pop(0)
        # Retrieving Video metadata
        self.duration = self.videometa.get("duration")
        self.frames = self.videometa.get("nb_frames")
        self.framerate = round(float(self.frames) / float(self.duration), 1)

        # Splitting video into frames
        print(self.filepath)
        if self.os_type == "linux":
            print("linux")
            self.command = f"ffmpeg -i {str(self.filepath)} thumb%04d.jpg -hide_banner"
        elif self.os_type == "win32":
            self.command = f"{ffmpegpath} -i {str(self.filepath)} thumb%04d.jpg -hide_banner"
        else:
            print("OS CURRENTLY UNSUPPORTED!")
            return False
        os.system(self.command)
        print("video split")
        self.files = self.tmppath
        self.filelist = os.listdir(self.tmppath)
        for self.file in self.filelist:
            self.files += f"{self.tmppath}{self.file}"

        if quality_mode == "default":
            if self.os_type == "linux":
                self.command = f"wine {fsrpath} -QualityMode {quality_setting} {self.files} {output_path}"
            elif self.os_type == "win32":
                self.command = f" {fsrpath} -QualityMode {quality_setting} {self.files} {output_path}"
            else:
                print("OS CURRENTLY UNSUPPORTED!")
                return False
        else:
            if quality_mode == "default":
                if self.os_type == "linux":
                    self.command = f"wine {fsrpath} -Scale {quality_setting} {self.files} {output_path}"
                elif self.os_type == "win32":
                    self.command = f" {fsrpath} -Scale {quality_setting} {self.files} {output_path}"
                else:
                    print("OS CURRENTLY UNSUPPORTED!")
                    return False

        os.system(self.command)
