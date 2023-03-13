from ..test_data import SETTING_DATA, UTT_RESULT, PATH, WS_MANGER
from gailbot.services.converter.payload.audioPayload import AudioPayload, load_audio_payload
from tests.core.engines.data import AudioPath
from gailbot.services.organizer.source import SourceObject, SourceManager
from gailbot.services.organizer.settings import SettingObject
from gailbot.core.utils.general import get_name, is_file, is_directory, paths_in_dir, subdirs_in_dir
import logging

TEST_SETTING = SettingObject (SETTING_DATA.PROFILE, "test_setting")
audio_source = SourceObject(AudioPath.MEDIUM_AUDIO, get_name(AudioPath.MEDIUM_AUDIO), output=AudioPath.RESULT_OUTPUT)
audio_source.apply_setting(TEST_SETTING)

def test_audio():
    test_payload: AudioPayload = load_audio_payload(audio_source, WS_MANGER)[0]
    assert test_payload
    assert test_payload.name == get_name(AudioPath.MEDIUM_AUDIO)
    logging.info(test_payload.original_source)
    assert(test_payload.setting.engine_setting.engine == SETTING_DATA.PROFILE["engine_setting"]["engine"]) 
    assert(test_payload.get_engine() == SETTING_DATA.PROFILE["engine_setting"]["engine"]) 
    logging.info(test_payload.workspace)
    logging.info(test_payload.out_dir)
    logging.info(test_payload.transcription_result.get_data())
    logging.info(test_payload.setting.get_plugin_setting())
    logging.info(test_payload.supported_format)
    logging.info(test_payload.get_status())
    logging.info(test_payload.get_source())
    logging.info(test_payload.data_files)
    for file in test_payload.data_files:
        assert is_file(file)
        logging.info(file)
        
    assert not test_payload.transcribed
    assert not test_payload.analyzed
    assert not test_payload.formatted
    
    assert test_payload.set_transcription_result(UTT_RESULT.UTT_DICT)
    logging.info(test_payload.get_transcription_result())
    

def test_invalid_audio():
    paths = paths_in_dir(PATH.INVALID_DATA_DIR)
    paths.extend(subdirs_in_dir(PATH.INVALID_DATA_DIR))
    sources = [SourceObject(path, get_name(path), PATH.OUTPUT_ROOT) for path in paths]
    for source in sources:
        assert source
        assert source.name 
        assert not load_audio_payload(source, WS_MANGER)
        source.apply_setting(TEST_SETTING)
        assert not load_audio_payload(source, WS_MANGER)