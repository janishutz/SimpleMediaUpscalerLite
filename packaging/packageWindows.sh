#! /bin/bash

cd ..

# Compile for Windows
wine python -m PyInstaller imagevideoupscaler.spec
cp -r ./dist/imagevideoupscaler/* ./frontend/

# Copy python files
cp -rv ./bin ./frontend/
cp -rv ./config ./frontend/
cp -v ./imagevideoupscaler-cli.py ./frontend/
cp -v ./LICENSE ./frontend/
cp -v ./logo.png ./frontend/

# package for Windows (includes GUI & CLI)
cd frontend
npm run electron:build -- --win nsis

rm -rf ./bin
rm -rf ./config
rm -rf ./lib-dynload
rm ./image*
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