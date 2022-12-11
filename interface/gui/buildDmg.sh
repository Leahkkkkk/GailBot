#! /bin/bash
mkdir -p ../../install/dist/dmg 
cp -r ../../install/dist/GailBot.app ../../install/dist/dmg
create-dmg \
  --volname "GailBot.app" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --hide-extension "GailBot.app" \
  --app-drop-link 425 120 \
  "../../install/dist/GailBot.dmg" \
  "../../install/dist/dmg/"