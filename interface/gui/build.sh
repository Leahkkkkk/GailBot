rm -r dist 
rm -r build
pyinstaller --noconsole --windowed app.py   \
--name "AppTest5" \
--add-data "config/:config" \
--add-data "asset/:asset" \
--hidden-import waitress \
--clean