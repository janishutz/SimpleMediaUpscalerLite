#! /bin/bash

cd ..

# Make linux executable
pyinstaller imagevideoupscaler.spec
cp -r ./dist/imagevideoupscaler/* ./frontend/

# wine python -m pyinstaller imagevideoupscaler.spec
# cp ./dist/imagevideoupscaler/* ./frontend/

cp -r ./bin ./frontend/
cp -r ./config ./frontend/
cp ./imagevideoupscaler-cli.py ./frontend/
cp ./LICENSE ./frontend/
cp ./logo.png ./frontend/

# package for all platforms (includes GUI & CLI)
cd frontend
npm run electron:build -- --linux deb rpm --win nsis

printf '\n\n==> Cleaning up\n\n'
# rm -rf ./lib/bin
# rm -rf ./src/config
# rm -rf ./src/libdynload
# rm ./lib/image*
# rm ./lib/lib*
# rm ./lib/ld*
# rm ./lib/base_library.zip
# rm ./lib/imagevideoupscaler-cli.py
# rm ./lib/LICENSE


# Make windows executable
# TODO: create compiler