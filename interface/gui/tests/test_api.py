# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-12 14:26:59
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-16 14:04:41
from gailbot import GailBot
from tests.services.test_data import PATH
from tests.services.test_data import SETTING_DATA
import logging

def transcribe(files, setting_name = "test", setting_data = SETTING_DATA.WHISPER_PROFILE, output = PATH.USER_ROOT):
    gb = GailBot(output)
    assert gb.reset_workspace
    input = [(f, PATH.OUTPUT_ROOT) for f in files]
    gb.add_sources(input)
    gb.create_new_setting(setting_name, setting_data)
    assert gb.apply_setting_to_sources(files, setting_name)
    for file in files:
        assert gb.get_src_setting_name(file) == setting_name
        assert gb.is_source(file)
    return gb.transcribe()
    
def test_gailbot():
    gb = GailBot(PATH.BACKUP_ROOT)
    assert gb.reset_workspace() 
    
def test_transcribe():
    res, invalid = transcribe([PATH.SMALL_AUDIO_WAV, PATH.SMALL_CONVERSATION_DIR])
    assert res 
    assert invalid == []
    
def test_transcribe_dir():
    res, invalid = transcribe([PATH.MANY_FILES_DIR, PATH.SMALL_CONVERSATION_DIR, PATH.TRANSCRIBED_DIR, PATH.MANY_SMALL_FILES_DIR])
    assert res 
    assert invalid == []
    
def test_with_speaker_one_file():
    res, invalid = transcribe([PATH.LONG_LIB_RECORD], "speaker", SETTING_DATA.WHISPER_SPEAKER_PROFILE)
    assert res 
    assert invalid == []
    
def test_with_speaker_short():
    res, invalid = transcribe([PATH.SHORT_AUDIO], "speaker", SETTING_DATA.WHISPER_SPEAKER_PROFILE)
    assert res 
    assert invalid == []
    
def test_with_speaker_dir():
    res, invalid = transcribe([PATH.SMALL_CONVERSATION_DIR, PATH.MANY_SMALL_FILES_DIR], "speaker", SETTING_DATA.WHISPER_SPEAKER_PROFILE, output=PATH.BACKUP_ROOT)    
    assert res 
    assert invalid == []
    
def test_invalid():
    res, invalid = transcribe([PATH.INVALID_DATA_DIR, PATH.DUMMY_AUDIO, PATH.EMPTY, PATH.MIX])
    logging.info(res)
    logging.info(invalid)

