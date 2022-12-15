#! /bin/bash
rm -r ../install/dist 
rm -r ../install/build
rm *spec
pyinstaller --noconsole --windowed ../gui/app.py   \
--name "GailBot" \
--icon "../install/GailBotLogo.icns" \
--add-data "../gui/config/:config" \
--add-data "../gui/asset/:asset" \
--hidden-import waitress \
--clean
mv build ../install
mv dist ../install