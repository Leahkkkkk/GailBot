rm -r dist 
rm -r build
rm *spec
pyinstaller --noconsole --windowed app.py   \
--name "AppTest1129" \
--add-data "config/:config" \
--add-data "asset/:asset" \
--hidden-import waitress \
--clean