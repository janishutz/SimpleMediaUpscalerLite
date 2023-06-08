#! /bin/bash

cd ..

# Compile for Linux
python -m PyInstaller smuL-cli.spec
cp -r ./dist/smuL-cli/* ./frontend/lib/


# Copy python files
cp -r ./bin ./frontend/lib/
cp -r ./config ./frontend/lib/
cp ./smuL-cli.py ./frontend/lib/
cp ./LICENSE ./frontend/lib/
cp ./logo.png ./frontend/lib/


# package for Linux (includes GUI & CLI)
cd frontend
rm -rf ./dist_electron
npm run electron:build -- --linux deb rpm

rm -rf ./lib

cd ..

rm -rf ./build
rm -rf ./dist

printf '\n\n==> DONE\n\n'