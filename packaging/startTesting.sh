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