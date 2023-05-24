<div id="title" align="center">
    <img src="./logo.png" width="300">
    <h1>ImageVideoUpscalerFrontend</h1>
</div>

<div id="badges" align="center">
    <img src="https://img.shields.io/github/release/simplePCBuilding/FSRImageVideoUpscalerFrontend.svg">
    <img src="https://img.shields.io/github/license/simplePCBuilding/FSRImageVideoUpscalerFrontend.svg">
    <img src="https://img.shields.io/github/repo-size/simplePCBuilding/FSRImageVideoUpscalerFrontend.svg">
    <img src="https://img.shields.io/tokei/lines/github/simplePCBuilding/FSRImageVideoUpscalerFrontend">
    <img src="https://img.shields.io/github/issues-pr-raw/simplePCBuilding/FSRImageVideoUpscalerFrontend">
    <img src="https://img.shields.io/github/languages/top/simplePCBuilding/FSRImageVideoUpscalerFrontend">
    <img src="https://img.shields.io/github/directory-file-count/simplePCBuilding/FSRImageVideoUpscalerFrontend.svg">
    <img src="https://img.shields.io/github/package-json/v/simplePCBuilding/FSRImageVideoUpscalerFrontend.svg">
</div>
A PyQT5 frontend to upscale images / videos using AMD's FidelityFX Super Resolution. 

# Functionality
This App is a PyQT5 frontend to AMD's FidelityFX Super Resolution codebase, which allows you to upscale basically anything that is some kind of an image. 
- Choose an input & output file from a GUI filemanager.
- Choose from different quality presets or set your own multiplier
- You may upscale Images (currently .png, .jpg and .jpeg) or Videos (currently .mp4 and .mkv)
- Output file will be written to the specified.

This App also features a CLI interface.
- Options:
```
-s SCALEFACTOR	--scalefactor SCALEFACTOR		Factor of form 2x, maximum 4x
-S SHARPENING	--sharpening SHARPENING			Value (0 - 1)
-T THREADCOUNT	--threads THREADCOUNT			Choose how many threads in parallel. Maximum is max threads of your CPU
-F FILETYPE		--filetype FILETYPE				Choose file type of temporary image files when upscaling videos (required)
-N 				--noscaling						No upscaling, requires -S option (Sharpening option)
```

# Contributing
If you have any suggestions or features you'd like to have implemented, you may either implement the feature yourself and open a pull request, or open an issue on this GitHub page. Both things are appreciated!
*I am looking for somebody willing to maintain the Windows version (including installer) as I am running Linux*

Current Contributers
- simplePCBuilding
- ThatPlasma


# Roadmap
V1.0.0:
- Get the app working -- :white_check_mark:
- Quality selector (presets and custom multiplier) -- :white_check_mark:
- Filechoosers -- :white_check_mark:
- Imageformats: .png, .jpg, .jpeg; Videoformats: .mp4, .mkv -- :white_check_mark:
- Working UI -- :white_check_mark:
- Basic Wiki -- :white_check_mark:
- Add all compiling infos to the repo -- :white_check_mark:
- Add about section inside app -- Might be implemented in V1.1.0

V1.1.0: 
- Migrate to PyQt5 (or create Electron app and make python app CLI only)
- Create Windows & Mac Version
- Refactor backend to add plugin support
- Add more scaling engines
- Expand Wiki to feature documentation on how to create a plugin (and maybe add a project website)

V1.2.0:
- Show progress of scaling

# Issues
The app is technically functional, but there may still be some big bugs. If you run into any of them, please open an issue on this Github page under "issues". I will attempt to fix them as fast as possible, but a fully compiled version might still take a couple of days to arrive. 

# Supported OS
Supported technically is every OS that can run python, but tested so far only Linux is. I will create a Windows exe, a rpm and deb package and maybe a dmg.

# INFO
I will not be pushing the code to the main branch until there is a somewhat stable version in the dev-V1 branch. If you want to see the code, check it out there!
