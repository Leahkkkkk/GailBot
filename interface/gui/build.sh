pyinstaller --onefile --noconsole app.py --windowed  \
--name "Test" \
--add-data "config/:config" \
--add-data "asset/:asset" \
--hidden-import waitress \
--clean