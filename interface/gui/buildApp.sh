#! /bin/bash
rm -r ../../install/dist 
rm -r ../../install/build
rm *spec
pyinstaller --noconsole --windowed app.py   \
--name "GailBot" \
--icon "GailBotLogo.icns" \
--add-data "config/:config" \
--add-data "asset/:asset" \
--hidden-import waitress \
--clean
mv build ../../install
mv dist ../../install