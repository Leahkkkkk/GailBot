mkdir -p dist/dmg 
cp -r dist/AppTest5.app dist/dmg
create-dmg \
  --volname "AppTest5.app" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --hide-extension "AppTest5.app" \
  --app-drop-link 425 120 \
  "dist/AppTest5.dmg" \
  "dist/dmg/"