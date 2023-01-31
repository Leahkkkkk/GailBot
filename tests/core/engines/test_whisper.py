# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-30 22:25:13
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-31 18:18:21


import sys
import os
import json

from gailbot.core.engines.whisperEngine import WhisperEngine

def test_whisper():
    engine = WhisperEngine(
        model="tiny",
        model_cache_dir="./whisper_temp_cache"
    )
    print(engine.get_supported_formats())
    print(engine.get_available_models())
    print(engine.get_supported_languages())

    result = engine.transcribe(
        audio_path="/Users/muhammadumair/Documents/Repositories/mumair01-repos/GailBot/data/dev_test_data/media/audio/wav/test_output.wav",
        outdir="./whisper_out",
        language="English"
    )

    print(json.dumps(result, indent = 2, ensure_ascii = False))