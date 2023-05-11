#! /bin/bash
mkdir -p dist/dmg 
cp -r dist/GailBot.app dist/dmg
create-dmg \
  --volname "GailBot.app" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --hide-extension "GailBot.app" \
  --app-drop-link 425 120 \
  "dist/GailBot.dmg" \
  "dist/dmg/"