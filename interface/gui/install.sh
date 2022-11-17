mkdir -p dist/dmg 
cp -r dist/AppTest4.app dist/dmg
create-dmg \
  --volname "AppTest4.app" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --hide-extension "AppTest4.app" \
  --app-drop-link 425 120 \
  "dist/AppTest4.dmg" \
  "dist/dmg/"