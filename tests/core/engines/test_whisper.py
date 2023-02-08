# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-30 22:25:13
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-02-07 18:12:13


import sys
import os
import json
import time

from gailbot.core.engines.whisperEngine import WhisperEngine
from gailbot.core.utils.general import write_json

def test_whisper():
    engine = WhisperEngine()
    print(engine)
    print(engine.get_supported_formats())
    print(engine.get_available_models())
    print(engine.get_supported_languages())

    start = time.time()
    result = engine.transcribe(
        audio_path="/Users/muhammadumair/Documents/Repositories/mumair01-repos/GailBot/data/dev_test_data/media/audio/wav/test_output.wav",
        language="English",
        detect_speakers=False
    )
    print(f"Time taken for transcription: {time.time() - start}")
    print(json.dumps(result, indent = 2, ensure_ascii = False))
    # write_json("./res.json",{"data" : result})




    # print(json.dumps(result, indent = 2, ensure_ascii = False))