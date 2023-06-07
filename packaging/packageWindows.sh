#! /bin/bash

cd ..

# Compile for Windows
wine python -m PyInstaller smuL-cli.spec

mkdir ./frontend/lib

cp -r ./dist/smuL-cli/* ./frontend/lib/

# Copy python files
cp -rv ./bin ./frontend/lib/
cp -rv ./config ./frontend/lib/
cp -v ./smuL-cli.py ./frontend/lib/
cp -v ./LICENSE ./frontend/lib/
cp -v ./logo.png ./frontend/lib/

# package for Windows (includes GUI & CLI)
cd frontend
rm -rf ./dist_electron
npm run electron:build -- --win nsis

rm -rf ./lib

cd ..

rm -rf ./build
rm -rf ./dist

printf '\n\n==> DONE\n\n'