# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-30 22:25:13
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-02-07 18:12:13
import sys
import os
import json
import time
from .data import AudioPath
from gailbot.core.engines.whisperEngine import WhisperEngine
from gailbot.core.utils.general import write_json
import pytest 

def whisper_test(audio, detect_speaker: bool, output):
    engine = WhisperEngine()
    print(engine)
    print(engine.get_supported_formats())
    print(engine.get_available_models())
    print(engine.get_supported_languages())

    start = time.time()
    result = engine.transcribe(
        audio_path=audio,
        language="English",
        detect_speakers=detect_speaker
    )
    print(f"Time taken for transcription: {time.time() - start}")
    print(json.dumps(result, indent = 2, ensure_ascii = False))
    write_json(f"{AudioPath.WHISPER_OUT_PATH}/{output}",{"data" : result})
    

@pytest.mark.parametrize("audio, detect_speaker, output", 
                [(AudioPath.SHORT_PHONE_CALL, True, "short_phone_call.json")])
def test_detect_speaker(audio, detect_speaker, output):
    whisper_test(audio, detect_speaker, output)

@pytest.mark.parametrize("audio, detect_speaker, output", 
                [(AudioPath.LONG_PHONE_CALL, True, "long_phone_call.json")])
def test_detect_speaker_long(audio, detect_speaker, output):
    whisper_test(audio, detect_speaker, output)
    
@pytest.mark.parametrize("audio, detect_speaker, output", 
                [(AudioPath.LARGE_AUDIO_WAV, False, "long_audio.json")])
def test_long_audio(audio, detect_speaker, output):
    whisper_test(audio, detect_speaker, output)