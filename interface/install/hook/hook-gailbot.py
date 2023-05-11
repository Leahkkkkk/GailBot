from PyInstaller.utils.hooks import collect_all, copy_metadata
import logging
PACKAGES=[
  "torchaudio",
  "torchvision",
  "librosa",
  "sklearn",
  "pyannote",
  "huggingface_hub",
  "whisper",
  "pytorch_metric_learning",
  "hmmlearn",
  "speechbrain",
  "certifi",
  "syllables",
  "syllable",
  "rich",
  "certifi",
  "pytorch_lightning",
  "pyannote.audio",
  "pyannote.pipeline",
  "syllables",
  "certifi",
  "PIL",
  "tqdm",
  "regex",
  "requests",
  "packaging",
  "filelock",
  "tokenizers",
  "importlib_metadata",
  "torch-audiomentations",
  "torchmetrics",
  "torchaudio",
  "torch-pitch-shift",
  "pyannote.audio",
  "asteroid_filterbanks",
  "ffmpeg-python",
  "numpy"
]
no_meta = ["sklearn", "pyannote", "whisper", "ffmpeg", "PIL"]

def hook(hook_api):
    for pkg in PACKAGES:
        hook_api.add_imports(pkg)
        logging.info(f"start to import extra data from {pkg}")
        data, binary, hiddenimports = collect_all(pkg)
        logging.info(f"got file {data}, {binary}, {hiddenimports}")
        hook_api.add_datas(data) 
        hook_api.add_binaries(binary) 
        if pkg not in no_meta:
            hook_api.add_datas(copy_metadata(pkg))
        for module_name in hiddenimports:
            hook_api.add_imports(module_name)
        