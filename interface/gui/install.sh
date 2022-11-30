mkdir -p dist/dmg 
cp -r dist/AppTest1129.app dist/dmg
create-dmg \
  --volname "AppTest1129.app" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --hide-extension "AppTest1129.app" \
  --app-drop-link 425 120 \
  "dist/AppTest1129.dmg" \
  "dist/dmg/"