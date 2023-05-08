#! /bin/bash
python -m nuitka --include-data-dir=../gui/asset=asset \
 --include-data-dir=../gui/config_backend=config_backendd \
 --include-data-dir=../gui/config_frontend=config_frontend \
 --windows-icon-from-ico=GailBotLogo.icns \
 --plugin-enable=numpy \
 --noinclude-numba-mode=nofollow \
 --standalone ../gui/app.py