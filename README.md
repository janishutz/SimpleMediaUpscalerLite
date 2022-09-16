# FSRImageVideoUpscalerFrontend
A GTK frontend to upscale images / videos using AMD's FidelityFX Super Resolution. 
*NOTE: THIS PROJECT IS STILL IN DEVELOPMENT AND MAY STILL CONTAIN SOME FUNDEMENTAL BUGS!*

# Functionality
This App is a GTK frontend to AMD's FidelityFX Super Resolution codebase, which allows you to upscale basically anything that is some kind of an image. 
- Choose a input & output file from a GUI filemanager.
- Choose from different quality presets or set your own multiplier
- You may upscale Images (currently .png, .jpg and .jpeg) or Videos (currently .mp4 and .mkv)
- Output file will be written to a specified folder.

# Contributing
If you have any suggestions or features you'd like to have implemented, you may either implement the feature yourself and open a pull request, or open an issue on this GitHub page. Both things are appreciated!
*I am looking for somebody willing to maintain the Windows version (including installer) as I am running Linux*

# Roadmap
V1.0.0:
- Get the app working -- :white_check_mark:
- Create installer
- Quality selector (presets and custom multiplier) -- :white_check_mark:
- Filechoosers -- :white_check_mark:
- Imageformats: .png, .jpg, .jpeg; Videoformats: .mp4, .mkv -- :white_check_mark:
- Working UI -- :white_check_mark:
- Basic Wiki
- Add all compiling infos to the repo
- Add about section inside app

V1.1.0: 
- Custom Quality target resolution
- support more file formats (Which ones not decided yet)

V1.2.0:
- Show progress of scaling

V1.3.0: 
- Expand Wiki
- ...

# Issues
The app is technically functional, but there may still be some big bugs. If you run into any of them, please open an issue on this Github page under "issues". I will attempt to fix them as fast as possible, but a fully compiled version might still take a couple of days to arrive. 

# Supported OS
Supported technically is every OS that can run python, but tested so far only Linux is. I will create a Windows exe, a rpm and deb package and maybe a dmg.

# INFO
I will not be pushing the code to the main branch until there is a somewhat stable version in the dev-V1 branch. If you want to see the code, check it out there!
