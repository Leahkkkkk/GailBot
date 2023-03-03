# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.utils.hooks import copy_metadata
import sys ; sys.setrecursionlimit(sys.getrecursionlimit() * 5)

datas = [('../gui/config/', 'config'), ('../gui/asset/', 'asset'), ('../gui/config_gb/', 'config_gb'), ('../torchaudio/', './torchaudio')]
datas += collect_data_files('torch')
datas += copy_metadata('torch')
datas += copy_metadata('tqdm')
datas += copy_metadata('regex')
datas += copy_metadata('sacremoses')
datas += copy_metadata('requests')
datas += copy_metadata('packaging')
datas += copy_metadata('filelock')
datas += copy_metadata('numpy')
datas += copy_metadata('tokenizers')
datas += copy_metadata('importlib_metadata')
datas += copy_metadata('rich')
datas += copy_metadata('torch')
datas += copy_metadata('torch-audiomentations')
datas += copy_metadata('torchmetrics')
datas += copy_metadata('torchaudio')
datas += copy_metadata('torch-pitch-shift')
datas += copy_metadata('pyannote.audio')
datas += copy_metadata('librosa')
datas += copy_metadata('asteroid_filterbanks')
datas += copy_metadata('pytorch-metric-learning')
datas += copy_metadata('hmmlearn')
datas += copy_metadata('speechbrain')


block_cipher = None

a = Analysis(
    ['../gui/app.py'],
    pathex=[],
    binaries=[('./ffmpeg', '.')] ,
    datas=datas,
    hiddenimports=['pyannote.audio', 'speechbrain', 'hmmlearn', 'pytorch-metric-learning', 'asteroid_filterbanks','librosa', 'pytorch', 'sklearn.utils._cython_blas', 'sklearn.neighbors.typedefs', 'sklearn.neighbors.quad_tree', 'sklearn.tree', 'sklearn.tree._utils', 'torch', 'torch-audiomentations', 'torchmetrics', 'torch-pitch-shift'],
    hookspath=[],
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
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
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
    upx=True,
    upx_exclude=[],
    name='GailBot',
)
app = BUNDLE(
    coll,
    name='GailBot.app',
    icon='../install/GailBotLogo.icns',
    bundle_identifier=None,
)
