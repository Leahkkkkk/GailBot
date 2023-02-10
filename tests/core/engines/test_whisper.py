# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-30 22:25:13
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-02-07 18:12:13


""" TODO: test long audio """
import sys
import os
import json
import time
from .data import AudioPath
from gailbot.core.engines.whisperEngine import WhisperEngine
from gailbot.core.utils.general import write_json
import pytest 


@pytest.mark.parametrize("audio", 
                         [AudioPath.MEDIUM_AUDIO])
def test_whisper(audio):
    engine = WhisperEngine()
    print(engine)
    print(engine.get_supported_formats())
    print(engine.get_available_models())
    print(engine.get_supported_languages())

    start = time.time()
    result = engine.transcribe(
        audio_path=audio,
        language="English",
        detect_speakers=False
    )
    print(f"Time taken for transcription: {time.time() - start}")
    print(json.dumps(result, indent = 2, ensure_ascii = False))
    # write_json("./res.json",{"data" : result})
    # print(json.dumps(result, indent = 2, ensure_ascii = False))