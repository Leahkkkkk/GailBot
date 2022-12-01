rm -r dist 
rm -r build
rm *spec
pyinstaller --noconsole --windowed app.py   \
--name "GailBotTest" \
--add-data "config/:config" \
--add-data "asset/:asset" \
--hidden-import waitress \
--clean