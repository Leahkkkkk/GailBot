pyinstaller --onefile --noconsole --windowed app.py \
--name "Test" \
--add-data "config/:config" \
--add-data "asset/:asset" \
--hidden-import waitress \
--clean