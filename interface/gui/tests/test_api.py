# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-12 14:26:59
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-16 14:04:41
from gailbot import GailBot
from tests.services.test_data import PATH
from tests.services.test_data import SETTING_DATA
import logging

HIL_LAB = "/Users/yike/Documents/GitHub/GailBot/plugins/gb_hilab_suite"

def transcribe(files, setting_name = "test", setting_data = SETTING_DATA.WHISPER_PROFILE, output = PATH.USER_ROOT, fail_test = False):
    gb = GailBot(output)
    assert gb.reset_workspace()
    input = [(f, PATH.OUTPUT_ROOT) for f in files]
    gb.add_sources(input)
    assert gb.create_new_setting(setting_name, setting_data)
    assert gb.is_setting(setting_name)
    assert gb.apply_setting_to_sources(files, setting_name)
    for file in files:
        assert gb.get_src_setting_name(file) == setting_name
        assert gb.is_source(file)
    fails, invalid = gb.transcribe()
    logging.info(fails)
    logging.info(invalid)
    if not fail_test: 
        assert not (fails or invalid)
    return fails, invalid 
    
def test_gailbot():
    gb = GailBot(PATH.BACKUP_ROOT)
    assert gb.reset_workspace() 
 
#####################  test for whisper #####################
def test_whisper():
    fails, invalid = transcribe([PATH.SMALL_AUDIO_WAV, PATH.SMALL_CONVERSATION_DIR])
    assert not fails
    assert not invalid
    assert invalid == []
    
def test_whisper_one():
    fails, invalid = transcribe([PATH.HELLO_1], "whisper", SETTING_DATA.WHISPER_PROFILE)


def test_whisper_dir():
    fails, invalid = transcribe([PATH.MANY_FILES_DIR, PATH.SMALL_CONVERSATION_DIR, PATH.TRANSCRIBED_DIR, PATH.MANY_SMALL_FILES_DIR])
    
def test_with_speaker_one_file():
    fails, invalid = transcribe([PATH.LONG_LIB_RECORD], "speaker", SETTING_DATA.WHISPER_SPEAKER_PROFILE)
    
def test_with_speaker_short():
    fails, invalid = transcribe([PATH.SHORT_AUDIO], "speaker", SETTING_DATA.WHISPER_SPEAKER_PROFILE)
    
def test_with_speaker_dir():
    fails, invalid = transcribe([PATH.SMALL_CONVERSATION_DIR, PATH.MANY_SMALL_FILES_DIR], "speaker", SETTING_DATA.WHISPER_SPEAKER_PROFILE, output=PATH.BACKUP_ROOT)    
    
def test_invalid():
    fails, invalid = transcribe([PATH.INVALID_DATA_DIR, PATH.DUMMY_AUDIO, PATH.EMPTY, PATH.MIX], fail_test=True)
    assert invalid
    
    
###########################  test for watson #####################################
def test_watson():
    fails, invalid = transcribe([PATH.HELLO_1], "watson", SETTING_DATA.WATSON_PROFILE)

def test_watson_large():
    fails, invalid = transcribe([PATH.LONG_PHONE_CALL], "watson", SETTING_DATA.WATSON_PROFILE)

def test_watson_large_two():
    fails, invalid = transcribe([PATH.LONG_LIB_RECORD], "watson", SETTING_DATA.WATSON_PROFILE)
    
def test_watson_dir():
    fails, invalid = transcribe([PATH.MANY_SMALL_FILES_DIR], "watson", SETTING_DATA.WATSON_PROFILE)
    
def test_watson_many():
    fails, invalid = transcribe([PATH.HELLO_1, PATH.HELLO_2, PATH.HELLO_3, PATH.HELLO_4], "watson", SETTING_DATA.WATSON_PROFILE)

def test_watson_wav_suite():
    fails, invalid = transcribe(PATH.WAV_SUITE, "watson", SETTING_DATA.WATSON_PROFILE, fail_test=True)
    
def test_watson_wav_dir():
    fails, invalid = transcribe([PATH.WAV_DIR], "watson", SETTING_DATA.WATSON_PROFILE)
    
def test_watson_wav_test2a():
    fails, invalid = transcribe([PATH.TEST_2a], "watson", SETTING_DATA.WATSON_PROFILE)
    
def test_watson_wav_test2a_trim():
    fails, invalid = transcribe([PATH.TEST_2a], "watson", SETTING_DATA.WATSON_PROFILE)

def test_watson_wav_test2b():
    fails, invalid = transcribe([PATH.TEST_2b], "watson", SETTING_DATA.WATSON_PROFILE)

################################### test for google ##################################
def test_google():
    fails, invalid = transcribe([PATH.HELLO_1], "google", SETTING_DATA.GOOGLE_PROFILE) 
    
def test_google_many_hello():
    fails, invalid = transcribe([PATH.HELLO_1, PATH.HELLO_2, PATH.HELLO_3, PATH.HELLO_4], "google", SETTING_DATA.GOOGLE_PROFILE) 
    
def test_google_two():
    fails, invalid = transcribe([PATH.TWO_MIN_9], "google", SETTING_DATA.GOOGLE_PROFILE) 

def test_google_many_two():
    fails, invalid = transcribe([PATH.TWO_MIN_10, PATH.TWO_MIN_7, PATH.TWO_MIN_9, PATH.TWO_MIN_8], "google", SETTING_DATA.GOOGLE_PROFILE) 
    
def test_google_dir():
    fails, invalid = transcribe([PATH.MANY_FILES_DIR], "google", SETTING_DATA.GOOGLE_PROFILE)

def test_google_long():
    fails, invalid = transcribe([PATH.LONG_PHONE_CALL], "google", SETTING_DATA.GOOGLE_PROFILE)

def test_google_wav_suite():
    fails, invalid = transcribe(PATH.WAV_SUITE, "google", SETTING_DATA.GOOGLE_PROFILE)

##### 
def test_plugin():
    gb = GailBot(PATH.USER_ROOT)
    plugin_suite =  gb.register_plugin_suite(HIL_LAB)
    logging.info(plugin_suite)
    