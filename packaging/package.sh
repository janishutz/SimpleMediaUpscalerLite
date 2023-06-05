#! /bin/bash

cd ..

# Compile for Linux
pyinstaller smuL-cli.spec
cp -rv ./dist/smuL-cli/* ./frontend/


# Copy python files
cp -rv ./bin ./frontend/
cp -rv ./config ./frontend/
cp -v ./smuL-cli.py ./frontend/
cp -v ./LICENSE ./frontend/
cp -v ./logo.png ./frontend/


# package for Linux (includes GUI & CLI)
cd frontend
npm run electron:build -- --linux deb rpm

rm -rf ./libdynload
rm ./image*
rm ./lib*
rm ./ld*
rm ./base_library.zip

cd ..

rm -rf ./build
rm -rf ./dist

printf '\n\n==> Finished Linux packaging, preparing Windows\n\n'

# Compile for Windows
wine python -m PyInstaller smuL-cli.spec
cp -rv ./dist/smuL-cli/* ./frontend/
cp -v ./smuL-cli.py ./frontend/

# package for Windows (includes GUI & CLI)
cd frontend
npm run electron:build -- --win nsis

rm -rf ./bin
rm -rf ./config
rm -rf ./lib-dynload
rm ./smuL*
rm ./_*
rm ./py*
rm ./lib*
rm ./base_library.zip
rm ./*.pyd
rm ./*.dll
rm ./LICENSE

cd ..

rm -rf ./build
rm -rf ./dist

printf '\n\n==> DONE\n\n'