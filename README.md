# FSRImageVideoUpscalerFrontend
A GTK frontend to upscale images / videos using AMD's FidelityFX Super Resolution. 
*NOTE: THIS PROJECT IS STILL IN DEVELOPMENT AND NOT YET READY TO USE!*

# Functionality
This App is a GTK frontend to AMD's FidelityFX Super Resolution codebase, which allows you to upscale basically anything that is some kind of an image. 
- Choose a file to upscale (intending to support at least .png, .jpg, .mp4 and .mkv, but future versions may include support for other formats as well
- Output file will be written to a specified folder.
- App will split videos into single-frame image files so FSR can upscale it and then reassemble the whole video and add the audio to it again. This means no vrr is supported!

# Issues
The app is technically functional, but there are lots of known issues. For example you can choose to export an image as any file format you could think off, which obviously doesn't work. This leads to a crash. I am working on the filter that is preventing this issue. Additionally, there's not yet any quality selection except you go into the source code and change a value. This is another thing I am currently working on and will be available sooner than the protections.

# INFO
I will not be pushing the code to the main branch until there is a somewhat stable version in the dev-V1 branch. If you want to see the code, check it out there!
