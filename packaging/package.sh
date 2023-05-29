#! /bin/bash

cd ..

# Make linux executable
pyinstaller imagevideoupscaler-cli.spec
mv -r ./dist/imagevideupscaler ./dist/imagevideupscaler-linux
cp -r ./bin ./dist/imagevideupscaler-linux
cp -r ./config ./dist/imagevideupscaler-linux
cp ./imagevideupscaler-cli.py ./dist/imagevideupscaler-linux
cp ./LICENSE ./dist/imagevideupscaler-linux
cp ./logo.png ./dist/imagevideupscaler-linux

# package rpm & deb
# TODO: create packager

# Make windows executable
# TODO: create compiler