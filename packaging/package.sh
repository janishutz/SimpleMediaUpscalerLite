#! /bin/bash

cd ..

# Compile for Linux
pyinstaller imagevideoupscaler.spec
cp -r ./dist/imagevideoupscaler/* ./frontend/


# Copy python files
cp -r ./bin ./frontend/
cp -r ./config ./frontend/
cp ./imagevideoupscaler-cli.py ./frontend/
cp ./LICENSE ./frontend/
cp ./logo.png ./frontend/


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
wine python -m PyInstaller imagevideoupscaler.spec
cp -r ./dist/imagevideoupscaler/* ./frontend/


# package for Windows (includes GUI & CLI)
cd frontend
npm run electron:build -- --win nsis

rm -rf ./bin
rm -rf ./config
rm -rf ./lib-dynload
rm ./image*
rm ./_*
rm ./imagevideoupscaler-cli.py
rm ./LICENSE

cd ..

rm -rf ./build
rm -rf ./dist

printf '\n\n==> DONE\n\n'