#!/bin/bash
# cd dist
# pkgbuild --component GailBot.app --identifier gailbot --version 0.1 --install-location /Applications GailBot.pkg
productbuild --component "dist/GailBot.app" "/Applications" "../../../../../Desktop/GailBot.pkg"