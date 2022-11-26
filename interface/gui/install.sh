mkdir -p dist/dmg 
cp -r dist/AppTest11223.app dist/dmg
create-dmg \
  --volname "AppTest11223.app" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --hide-extension "AppTest11223.app" \
  --app-drop-link 425 120 \
  "dist/AppTest11223.dmg" \
  "dist/dmg/"