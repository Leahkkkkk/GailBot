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
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import Future
from typing import List
import logging

def whisper_test(audio, detect_speaker: bool, output):
    engine = WhisperEngine(AudioPath.RESULT_OUTPUT)
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
                [(AudioPath.SHORT_AUDIO, False, "short_phone_call.json")])
def test_short(audio, detect_speaker, output):
    whisper_test(audio, detect_speaker, output)

@pytest.mark.parametrize("audio, detect_speaker, output", 
                [(AudioPath.LONG_PHONE_CALL, False, "long_phone_call.json")])
def test_detect_speaker_long(audio, detect_speaker, output):
    whisper_test(audio, detect_speaker, output)
    
@pytest.mark.parametrize("audio, detect_speaker, output", 
                [(AudioPath.FORTY_MIN, False, "long_audio.json")])
def test_long_audio(audio, detect_speaker, output):
    whisper_test(audio, detect_speaker, output)
    
def test_single_whisper():
    whisper = WhisperEngine(AudioPath.RESULT_OUTPUT)
    utt = whisper.transcribe(AudioPath.SineWaveMinus16)
    logging.info(utt)
    
    
def test_threading_whisper():
    whisper = WhisperEngine(AudioPath.RESULT_OUTPUT)
    futures: List[Future] = list()
    audios = [AudioPath.SHORT_AUDIO, AudioPath.HELLO_1, AudioPath.HELLO_2, AudioPath.HELLO_3, AudioPath.HELLO_4]
    with ThreadPoolExecutor(max_workers= 5) as executor:
        for audio in audios:
            future = executor.submit(whisper.transcribe, audio_path = audio)
            futures.append(future)
        for f in futures:
            if f.exception():
                print(f.exception())
            print(f.result())