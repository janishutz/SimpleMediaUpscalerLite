#! /bin/bash

cd ..

# Make linux executable
pyinstaller imagevideoupscaler.spec
cp ./dist/imagevideoupscaler/* ./frontend/src/

# wine python -m pyinstaller imagevideoupscaler.spec
# cp ./dist/imagevideoupscaler/* ./frontend/src/

cp -r ./bin ./frontend/src/
cp -r ./config ./frontend/src/
cp ./imagevideoupscaler-cli.py ./frontend/src/
cp ./LICENSE ./frontend/src/
cp ./logo.png ./frontend/src/

# package for all platforms (includes GUI & CLI)
cd frontend
npm run electron:build -- --linux deb rpm --win nsis

print '\n\n==> Cleaning up\n\n'
rm -rf ./src/bin
rm -rf ./src/config
rm ./src/imagevideoupscaler-cli.py
rm ./src/LICENSE
# Make windows executable
# TODO: create compiler