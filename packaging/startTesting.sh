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