mkdir -p dist/dmg 
cp -r dist/GailBotTest.app dist/dmg
create-dmg \
  --volname "GailBotTest.app" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --hide-extension "GailBotTest.app" \
  --app-drop-link 425 120 \
  "dist/GailBotTest.dmg" \
  "dist/dmg/"