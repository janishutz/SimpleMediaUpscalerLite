<div id="title" align="center">
    <img src="./logo.png" width="300">
    <h1>ImageVideoUpscalerFrontend</h1>
</div>

<div id="badges" align="center">
    <img src="https://img.shields.io/github/license/simplePCBuilding/ImageVideoUpscaler.svg">
    <img src="https://img.shields.io/github/repo-size/simplePCBuilding/ImageVideoUpscaler.svg">
    <img src="https://img.shields.io/tokei/lines/github/simplePCBuilding/ImageVideoUpscaler">
    <img src="https://img.shields.io/github/languages/top/simplePCBuilding/ImageVideoUpscaler">
    <img src="https://img.shields.io/github/directory-file-count/simplePCBuilding/ImageVideoUpscaler.svg">
    <br>
    <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/simplePCBuilding/ImageVideoUpscaler">
    <img alt="GitHub watchers" src="https://img.shields.io/github/watchers/simplePCBuilding/ImageVideoUpscaler">
    <img src="https://img.shields.io/github/issues-pr-raw/simplePCBuilding/ImageVideoUpscaler">
    <img alt="GitHub forks" src="https://img.shields.io/github/forks/simplePCBuilding/ImageVideoUpscaler">
    <img alt="GitHub commit activity" src="https://img.shields.io/github/commit-activity/m/simplePCBuilding/ImageVideoUpscaler">
    <br>
    <img alt="GitHub all releases" src="https://img.shields.io/github/downloads/simplePCBuilding/ImageVideoUpscaler/total?label=Downloads (total)">
    <img alt="GitHub release (latest by date)" src="https://img.shields.io/github/downloads/simplePCBuilding/ImageVideoUpscaler/latest/total?label=Downloads (latest)">
    <img src="https://img.shields.io/github/release/simplePCBuilding/ImageVideoUpscaler.svg">
    <img src="https://img.shields.io/github/package-json/v/simplePCBuilding/ImageVideoUpscaler.svg?label=Development Version">
    
</div>
An Electron App with Python CLI to upscale images and videos using multiple different upscaling engines.

# NEW NAME & LOGO NEEDED!
If you have suggestions for a name, please let us know [here](https://github.com/simplePCBuilding/ImageVideoUpscaler/issues/16). If you want to contribute a new logo, please open a PR and add it, or just let us know in the beforementioned issue.

# Functionality
This app allows you to fully automatically upscale a single file or a full on folder with one of many different engines.
- Choose an input & output file from a GUI filemanager.
- Choose from different quality presets or set your own multiplier
- You may upscale Images (currently .png, .jpg and .jpeg) or Videos (currently .mp4 and .mkv)
- Choose from one of many different upscaling algorithms.
- Add plugins to add even more upscaling engines to it

## Engines
- AMD Fidelity FX Super Resolution
- Cubic scaling
- High Quality Cubic
- Real-ESGRAN
- more to come!

This App also features a CLI interface (reference out of date).
- Options:
```
-s SCALEFACTOR	--scalefactor SCALEFACTOR		Factor of form 2x, maximum 4x
-S SHARPENING	--sharpening SHARPENING			Value (0 - 1)
-T THREADCOUNT	--threads THREADCOUNT			Choose how many threads in parallel. Maximum is max threads of your CPU
-F FILETYPE		--filetype FILETYPE				Choose file type of temporary image files when upscaling videos (required)
-N 				--noscaling						No upscaling, requires -S option (Sharpening option)
```

# Supported OS
- Windows 10, 11 (officially)
- Windows XP, Vista, 7, 8 (unofficially through python directly, may cause problems)
- Any modern Linux distro with wine installed

# Contributing
If you have any suggestions or features you'd like to have implemented, you may either implement the feature yourself and open a pull request, or open an issue on this GitHub page. Both things are appreciated!
*I am looking for somebody willing to maintain the Windows version (including installer) as I am running Linux*

--> Follow the rules layed out in CONTRIBUTING.md
--> We will add a linter that will then run on circleci to ensure code quality is high

### Current Contributers
- simplePCBuilding (Maintainer) [Core (CLI), Docs, Website, Frontend, Linux packages]
- ThatPlasma (Testing, Packager) [Testing, Windows Package]


# Roadmap
V1.1.0: 
- Migrate to Electron app
- Make python app CLI only -- ✅
- Package Windows & Linux Version
- Refactor backend to add plugin support -- ✅
- Add more scaling engines 
- Expand Wiki to feature documentation on how to create a plugin (and maybe add a project website)

V1.2.0:
- Show progress of scaling

# Issues
If you encounter any problems with this app, please don't hesitate to open an issue on GitHub.

## Known issues
- Electron App is not available yet
- GTK version only runs on Linux

# FAQ
**Q: Can you add upscaling engine [upscaling engine here]?**

A: We can add it most likely, please open an issue that contains a link to the library and please try and upscale an image using it yourself and copy-paste the command into a comment.
Just remember that it might take time to implement it and this is all developed in our free time and we have no obligation to implement it.

**Q: App no worky on OS XXXX**

A: Please check [Supported OS](#supported-os) that your OS is actually supported officially. If so, please open an issue and provide command used (if CLI) and error message that the app spat out when running.
If the OS is not officially supported, we may not be able to help you, since we intentionally don't support it officially

**Q: Why no worky on MacOS? / Can you port to MacOS?**

A: Wine support on MacOS is still mediocre and most likely cannot run some of the upscalers included by default so we cannot support it. I will be testing it at some point in a VM, but that won't necesarily speak for full functionality. If you find a way to run all upscalers on Mac, feel free to open a PR to add that functionality or just let us know what you did in an issue.

**Q: Upscaled XXX looks not as great as I want**

A: Try out different engines (that's why we support so many) and try to use sharpening to improve quality. If it doesn't help, you might want to suggest another engine.

**Q: How can I support you?**

A: You may contribute to this project by writing documentation, improving the website, adding plugins, fixing bugs, testing or by donating. 
