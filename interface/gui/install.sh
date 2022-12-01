mkdir -p dist/dmg 
cp -r dist/AppTest1130.app dist/dmg
create-dmg \
  --volname "AppTest1130.app" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --hide-extension "AppTest1130.app" \
  --app-drop-link 425 120 \
  "dist/AppTest1130.dmg" \
  "dist/dmg/"