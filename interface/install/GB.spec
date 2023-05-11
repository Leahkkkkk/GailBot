# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs, collect_system_data_files
from PyInstaller.utils.hooks import copy_metadata
import sys ; sys.setrecursionlimit(sys.getrecursionlimit() * 5)
package_path = "../../environment-setup/gb-dev/lib/python3.10/site-packages/" 
datas = [('../gui/config_backend/', 'config_backend'), 
         ('../gui/asset/', 'asset'), 
         ('../gui/config_frontend/', 'config_frontend'),
         ('./mklink.sh', '.')]
binaries = [('./ffmpeg', '.')]
hidden_imports =['certifi', 
                'ffmpeg-python',
                'pyannote.audio', 
                'speechbrain', 
                'hmmlearn', 
                'pytorch-metric-learning', 
                'asteroid_filterbanks',
                'librosa', 
                'pytorch', 
                'sklearn.utils._cython_blas', 
                'sklearn.neighbors.typedefs', 
                'sklearn.neighbors.quad_tree', 
                'sklearn.tree', 
                'sklearn.tree._utils', 
                'torch', 
                'torch-audiomentations', 
                'torchmetrics', 
                'torch-pitch-shift',
                'syllables']
block_cipher = None

a = Analysis(
    ['../gui/app.py'],
    pathex=[],
    binaries= binaries,
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=["./hook"],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='GailBot',
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['../install/GailBotLogo.icns'],
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='GailBot',
)

app = BUNDLE(
    coll,
    name='GailBot.app',
    icon='../install/GailBotLogo.icns',
    bundle_identifier=None,
)
