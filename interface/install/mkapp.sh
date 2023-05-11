#! /bin/bash
rm -r dist 
rm -r build
pyinstaller  GB.spec 
chmod +x mklink.sh
chmod +x mkdmg.sh
./mklink.sh
./mkdmg.sh