mkdir -p dist/dmg 
cp -r dist/Test.app dist/dmg
create-dmg \
  --volname "Test" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --hide-extension "Test.app" \
  --app-drop-link 425 120 \
  "dist/Test.dmg" \
  "dist/dmg/"