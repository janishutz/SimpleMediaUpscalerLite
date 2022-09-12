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
import time

# Loading the config file to get user preferred temp path
config = configparser.ConfigParser()
config.read('./config/settings.ini')


class Handler:
    def __init__(self):
        self.os_type = sys.platform
        self.command = ""
        self.tmppath = ""
        self.videometa = {}

    def handler(self, fsrpath, filepath, quality_mode, quality_setting, output_path):
        # Function to be called when using this class as this function automatically determines if file is video or image
        if self.os_type == "linux":
            self.tmppath = config["PathSettings"]["tmpPathLinux"]
        elif self.os_type == "win32":
            self.tmppath = config["PathSettings"]["tmpPathWindows"]
        else:
            print("OS CURRENTLY UNSUPPORTED!")
            return False
        self.tmppath += "fsru/"
        self.ffmpegpath = config["PathSettings"]["ffmpeg"]
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
            self.video_scaling(self.ffmpegpath, fsrpath, filepath, quality_mode, quality_setting, output_path)
        elif str(filepath)[len(filepath) - 4:] == ".JPG" or str(filepath)[len(filepath) - 4:] == ".png" or str(filepath)[len(filepath) - 4:] == ".jpg" or str(filepath)[len(filepath) - 5:] == ".jpeg":
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
        try:
            self.framerate = round(float(self.frames) / float(self.duration), 1)
        except TypeError:
            self.infos = str(self.videometa.get("r_frame_rate"))
            self.framerate = float(self.infos[:len(self.infos) - 2])

        # Splitting video into frames
        try:
            os.remove(self.tmppath)
        except FileNotFoundError:
            pass
        try:
            os.mkdir(self.tmppath)
        except FileExistsError:
            pass

        if self.os_type == "linux":
            print("linux")
            self.command = f"ffmpeg -i {str(self.filepath)} {self.tmppath}thumb%08d.png"
        elif self.os_type == "win32":
            self.command = f"{ffmpegpath} -i {str(self.filepath)} {self.tmppath}thumb%08d.png"
        else:
            print("OS CURRENTLY UNSUPPORTED!")
            return False
        os.system(self.command)
        print("video split")

        # Locate Images and assemble FSR-Command
        self.files = ""
        self.filelist = os.listdir(self.tmppath)
        self.filelist.pop(0)
        self.filelist.reverse()
        self.number = 0
        for self.file in self.filelist:
            self.number += 1
            self.files += f"{self.tmppath}{self.file} {self.tmppath}upscaled/USImage{str(self.number).zfill(8)}.png "
        self.maxlength = 32000
        self.pos = 1

        # Refactoring of commands that are longer than 32K characters
        if len(self.files) > self.maxlength:
            self.fileout = []

            while self.files[self.maxlength - self.pos:self.maxlength - self.pos + 1] != " ":
                self.pos += 1
            self.file_processing = self.files[:self.maxlength - self.pos]
            if self.file_processing[len(self.file_processing) - 13:len(self.file_processing) - 8] == "thumb":
                self.pos += 5
            else:
                pass
            while self.files[self.maxlength - self.pos:self.maxlength - self.pos + 1] != " ":
                self.pos += 1
            self.fileout.append(self.files[:self.maxlength - self.pos])
            self.filesopt = self.files[self.maxlength - self.pos:]
            self.posx = 0
            self.posy = self.maxlength

            # Command refactoring for commands that are longer than 64K characters
            if len(self.filesopt) > self.maxlength:
                while len(self.filesopt) > self.maxlength:
                    self.posx += self.maxlength - self.pos
                    self.posy += self.maxlength - self.pos
                    self.pos = 1
                    while self.files[self.posy - self.pos:self.posy - self.pos + 1] != " ":
                        self.pos += 1
                    self.file_processing = self.files[self.posx:self.posy - self.pos]
                    if self.file_processing[len(self.file_processing) - 13:len(self.file_processing) - 8] == "thumb":
                        self.pos += 5
                    else:
                        pass
                    while self.files[self.posy - self.pos:self.posy - self.pos + 1] != " ":
                        self.pos += 1

                    self.file_processing = self.files[self.posx:self.posy - self.pos]
                    self.fileout.append(self.file_processing)
                    self.filesopt = self.files[self.posy - self.pos:]
                self.fileout.append(self.filesopt)
            else:
                self.fileout.append(self.files[self.maxlength - self.pos:])
        else:
            self.fileout.append(self.files)

        try:
            os.mkdir(f"{self.tmppath}upscaled/")
        except FileExistsError:
            pass

        # Upscaling images
        print("\n\n\nUpscaling images... \n\n\n")
        while self.fileout != []:
            self.files_handle = self.fileout.pop(0)
            if quality_mode == "default":
                if self.os_type == "linux":
                    self.command = f"wine {fsrpath} -QualityMode {quality_setting} {self.files_handle}"
                elif self.os_type == "win32":
                    self.command = f"{fsrpath} -QualityMode {quality_setting} {self.files_handle}"
                else:
                    print("OS CURRENTLY UNSUPPORTED!")
                    return False
            else:
                if quality_mode == "default":
                    if self.os_type == "linux":
                        self.command = f"wine {fsrpath} -Scale {quality_setting} {self.files_handle} {self.tmppath}"
                    elif self.os_type == "win32":
                        self.command = f"{fsrpath} -Scale {quality_setting} {self.files_handle} {self.tmppath}"
                    else:
                        print("OS CURRENTLY UNSUPPORTED!")
                        return False
            os.system(self.command)
            print("Finished upscaling this section.")
            time.sleep(3)

        # get Video's audio
        print("Retrieving Video's audio to append")
        try:
            os.remove(f"{self.tmppath}audio.aac")
            os.remove(f"{output_path}")
        except FileNotFoundError:
            pass
        if self.os_type == "linux":
            self.command = f"ffmpeg -i {self.filepath} -vn -acodec copy {self.tmppath}audio.aac"
        elif self.os_type == "win32":
            self.command = f"{ffmpegpath} -i {self.filepath} -vn -acodec copy {self.tmppath}audio.aac"
        else:
            print("OS CURRENTLY UNSUPPORTED!")
            return False
        os.system(self.command)

        # reassemble Video
        print("Reassembling Video... with framerate @", self.framerate)
        if self.os_type == "linux":
            self.command = f"ffmpeg -framerate {self.framerate} -i {self.tmppath}upscaled/USImage%08d.png {output_path} -i {self.tmppath}audio.aac"
        elif self.os_type == "win32":
            self.command = f"{ffmpegpath} -framerate {self.framerate} -i {self.tmppath}upscaled/USImage%08d.png {output_path} -i {self.tmppath}audio.aac"
        else:
            print("OS CURRENTLY UNSUPPORTED!")
            return False
        os.system(self.command)

        print("\n\n\n DONE \n\n\n\n")
