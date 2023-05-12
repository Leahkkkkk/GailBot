NAME="GailBot-apple"

IDENTIFIER="com.pkg.GailBot-apple"

VERSION="0.0.1a1"

INSTALL_LOCATION="/Applications"
ROOT_LOCATION="/Applications/GailBot.app"


# put any command for changing the ownership or permissions here
chmod -R +x "$ROOT_LOCATION"

# Build package.
/usr/bin/pkgbuild \
    --root "$ROOT_LOCATION" \
    --install-location "$INSTALL_LOCATION" \
    --component-plist component.plist\
    --identifier "$IDENTIFIER" \
    --version "$VERSION" \
    --ownership preserve \
    "$NAME.pkg"