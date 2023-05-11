#! /bin/bash
python -m nuitka --include-data-dir=../gui/asset=asset \
 --nofollow-import-to=google.protobuf \
 --nofollow-import-to=test* \
 --noinclude-dlls=google.protobuf \
 --noinclude-dlls=_message.abi3\
 --include-data-dir=../gui/config_backend=config_backendd \
 --include-data-dir=../gui/config_frontend=config_frontend \
 --windows-icon-from-ico=GailBotLogo.icns \
 --noinclude-numba-mode=nofollow \
 --enable-plugin=numpy \
 --enable-plugin=torch \
 --enable-plugin=multiprocessing \
 --enable-plugin=tk-inter  \
 --standalone ../gui/app.py