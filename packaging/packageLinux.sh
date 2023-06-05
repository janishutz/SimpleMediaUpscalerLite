#! /bin/bash

cd ..

# Compile for Linux
pyinstaller smuL-cli.spec
cp -r ./dist/smuL-cli/* ./frontend/


# Copy python files
cp -r ./bin ./frontend/
cp -r ./config ./frontend/
cp ./smuL-cli.py ./frontend/
cp ./LICENSE ./frontend/
cp ./logo.png ./frontend/


# package for Linux (includes GUI & CLI)
cd frontend
npm run electron:build -- --linux deb rpm

rm -rf ./bin
rm -rf ./config
rm -rf ./libdynload
rm ./smuL*
rm ./lib*
rm ./ld*
rm ./base_library.zip
rm ./LICENSE

cd ..

rm -rf ./build
rm -rf ./dist

printf '\n\n==> DONE\n\n'