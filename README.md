<div id="title" align="center">
    <img src="./assets/logo.png" width="300">
    <h1>SimpleMediaUpscalerLite</h1>
</div>

<div id="badges" align="center">
    <img src="https://img.shields.io/github/license/simplePCBuilding/SimpleMediaUpscalerLite.svg">
    <img src="https://img.shields.io/github/repo-size/simplePCBuilding/SimpleMediaUpscalerLite.svg">
    <img alt="Lines of code" src="https://img.shields.io/tokei/lines/github/simplePCBuilding/SimpleMediaUpscalerLite">
    <img src="https://img.shields.io/github/languages/top/simplePCBuilding/SimpleMediaUpscalerLite">
    <img src="https://img.shields.io/github/directory-file-count/simplePCBuilding/SimpleMediaUpscalerLite.svg">
    <br>
    <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/simplePCBuilding/SimpleMediaUpscalerLite">
    <img alt="GitHub watchers" src="https://img.shields.io/github/watchers/simplePCBuilding/SimpleMediaUpscalerLite">
    <img src="https://img.shields.io/github/issues-pr-raw/simplePCBuilding/SimpleMediaUpscalerLite">
    <img alt="GitHub forks" src="https://img.shields.io/github/forks/simplePCBuilding/SimpleMediaUpscalerLite">
    <img alt="GitHub commit activity" src="https://img.shields.io/github/commit-activity/m/simplePCBuilding/SimpleMediaUpscalerLite">
    <br>
    <img alt="GitHub all releases" src="https://img.shields.io/github/downloads/simplePCBuilding/SimpleMediaUpscalerLite/total?label=Downloads (total)">
    <img alt="GitHub release (latest by date)" src="https://img.shields.io/github/downloads/simplePCBuilding/SimpleMediaUpscalerLite/latest/total?label=Downloads (latest)">
    <img src="https://img.shields.io/github/release/simplePCBuilding/SimpleMediaUpscalerLite.svg">
    <img src="https://img.shields.io/github/package-json/v/simplePCBuilding/SimpleMediaUpscalerLite.svg?label=Development Version">
</div>

<div id="donate" align="center">
    <a href="https://store.janishutz.com/donate" target="_blank"><img src="https://store-cdn.janishutz.com/static/support-me.jpg" width="150px"></a>
</div>

smuL (pronounced like "small") is an Electron App with Python CLI to upscale images and videos using multiple different upscaling engines. 

# Functionality
smuL features a GUI that allows you to select input and output files, scaling factors and many more settings. It can be easily extended using plugins.


# Supported OS
- Windows 10, 11 (officially)
- Windows XP, Vista, 7, 8 (unofficially through python directly, may cause problems)
- Any modern Linux distro with wine installed

# Contributing
If you have any suggestions or features you'd like to have implemented, you may either implement the feature yourself and open a pull request, or open an issue on this GitHub page. Both things are appreciated!

--> Follow the rules layed out in CONTRIBUTING.md
--> We will add a linter that will then run on circleci to ensure code quality is high

### Current Contributers
- simplePCBuilding (Maintainer) [Core (CLI), Docs, Website, Frontend, Linux packages]
- ThatPlasma (Testing, Packager) [Testing]


# Roadmap
V2.0.0: 
- Migrate to Electron app -- ✅
- Package Windows & Linux Version -- ✅
- Add packaging script for Linux & Windows version -- ✅
- Make python app CLI only -- ✅
- Refactor backend to add plugin support -- ✅

V2.1.0:
- Add more scaling engines 
- Expand Wiki to feature documentation on how to create a plugin (and maybe add a project website)
- Show progress of scaling

# Issues
If you encounter any problems with this app, please don't hesitate to open an issue on GitHub.

## Known issues
- Electron App is not available yet
- Electron App shows that it is out of date if running in the development version
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
