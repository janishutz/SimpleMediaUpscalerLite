#! /bin/bash

cd ..

# Compile for Linux
pyinstaller smuL-cli.spec

mkdir ./frontend/lib/
cp -rv ./dist/smuL-cli/* ./frontend/lib/


# Copy python files
cp -rv ./bin ./frontend/lib/
cp -rv ./config ./frontend/lib/
cp -v ./smuL-cli.py ./frontend/lib/
cp -v ./LICENSE ./frontend/lib/
cp -v ./logo.png ./frontend/lib/


# package for Linux (includes GUI & CLI)
cd frontend
rm -rf ./dist_electron
npm run electron:build -- --linux deb rpm

rm -rf ./lib/libdynload
rm ./lib/smuL*
rm ./lib/lib*
rm ./lib/ld*
rm ./lib/base_library.zip

cd ..

rm -rf ./build
rm -rf ./dist

printf '\n\n==> Finished Linux packaging, preparing Windows\n\n'

# Compile for Windows
wine python -m PyInstaller smuL-cli.spec
cp -rv ./dist/smuL-cli/* ./frontend/lib/
cp -v ./smuL-cli.py ./frontend/lib/

# package for Windows (includes GUI & CLI)
cd frontend
npm run electron:build -- --win nsis

rm -rf ./lib

cd ..

rm -rf ./build
rm -rf ./dist

printf '\n\n==> DONE\n\n'