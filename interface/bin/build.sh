#! /bin/bash
rm -r ../install/dist 
rm -r ../install/build
pyinstaller  GailBot.spec 
mv build ../install
mv dist ../install