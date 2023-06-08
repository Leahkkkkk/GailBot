# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-31 11:57:24
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-02-07 17:48:33


from whisper import load_model, available_models, _download, _MODELS # defined in __init__.py
from whisper import audio, decoding, model, normalizers, tokenizer, utils
from whisper.audio import load_audio, log_mel_spectrogram, pad_or_trim
from whisper.decoding import DecodingOptions, DecodingResult, decode, detect_language
from whisper.model import Whisper, ModelDimensions

from .transcribe import transcribe_timestamped as transcribe
from .utils import supported_languages
