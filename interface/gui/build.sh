pyinstaller --onefile --noconsole --windowed app.py   \
--name "AppTest4" \
--add-data "config/:config" \
--add-data "asset/:asset" \
--hidden-import waitress \
--clean