# FSRImageVideoUpscalerFrontend
A GTK frontend to upscale images / videos using AMD's FidelityFX Super Resolution. 
*NOTE: THIS PROJECT IS STILL IN DEVELOPMENT AND NOT YET READY TO USE!*

# Functionality
This App is a GTK frontend to AMD's FidelityFX Super Resolution codebase, which allows you to upscale basically anything that is some kind of an image. 
- Choose a file to upscale (intending to support at least .png, .jpg, .mp4 and .mkv, but future versions may include support for other formats as well
- Output file will be written to a specified folder.
- App will split videos into single-frame image files so FSR can upscale it and then reassemble the whole video and add the audio to it again. This means no vrr is supported!

# Issues
The app is technically functional, but there may still be some big bugs. If you run into any of them, please open an issue on this Github page under "issues". I will attempt to fix them as fast as possible, but a fully compiled version might still take a couple of days to arrive. 

# Supported OS
Supported technically is every OS that can run python, but tested so far only Linux is. I will create a Windows exe, a rpm and deb package and maybe a dmg.

# INFO
I will not be pushing the code to the main branch until there is a somewhat stable version in the dev-V1 branch. If you want to see the code, check it out there!
