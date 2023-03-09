# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.utils.hooks import copy_metadata
import sys ; sys.setrecursionlimit(sys.getrecursionlimit() * 5)

datas = [('../gui/config_gui/', 'config_gui'), 
         ('../gui/asset/', 'asset'), 
         ('../gui/config_gb/', 'config_gb'),
         ('./pre.sh', '.')]
datas += collect_data_files('torch')
datas += collect_data_files('torchaudio')
datas += collect_data_files('librosa')
datas += collect_data_files('sklearn')
datas += collect_data_files('pyannote')
datas += collect_data_files('pytorch_metric_learning')
datas += collect_data_files('certifi')
datas += collect_data_files('hmmlearn')
datas += collect_data_files('huggingface_hub')
datas += collect_data_files('pytorch_lightning')
datas += collect_data_files('whisper')
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
datas += copy_metadata('ffmpeg-python')
datas += copy_metadata('librosa')

binaries = [('./ffmpeg', '.')]

block_cipher = None

a = Analysis(
    ['../gui/app.py'],
    pathex=["/Users/yike/opt/anaconda3/envs/gb-ui-dev/lib/python3.10/site-packages"],
    binaries= binaries,
    datas=datas,
    hiddenimports=['certifi', 'ffmpeg-python', 'pyannote.audio', 'speechbrain', 'hmmlearn', 'pytorch-metric-learning', 'asteroid_filterbanks','librosa', 'pytorch', 'sklearn.utils._cython_blas', 'sklearn.neighbors.typedefs', 'sklearn.neighbors.quad_tree', 'sklearn.tree', 'sklearn.tree._utils', 'torch', 'torch-audiomentations', 'torchmetrics', 'torch-pitch-shift'],
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
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
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
