pyinstaller --windowed app.py \
--name "gailbot" \
--add-data "config/:config" \
--add-data "asset/:asset" \
--hidden-import waitress \
--clean