#! /bin/bash
rm -r dist 
rm -r build
pyinstaller  GB.spec 
chmod +x mklink.sh
./mklink.sh
mv dist/GailBot.app /Applications/