from ..test_data import SETTING_DATA, UTT_RESULT, PATH
from gailbot.services.converter.payload.conversationDirectoryPayload import ConversationDirectoryPayload, load_conversation_dir_payload
from tests.core.engines.data import AudioPath
from gailbot.services.organizer.source import SourceObject, SourceManager
from gailbot.services.organizer.settings import SettingObject
from gailbot.services.converter.payload.payloadObject import PayLoadObject, PayLoadStatus
import pytest
from gailbot.core.utils.general import get_name, is_file, is_directory, paths_in_dir, subdirs_in_dir
from gailbot.core.utils.logger import makelogger 
import logging

TEST_SETTING = SettingObject (SETTING_DATA.PROFILE, "test_setting")
audio_source = SourceObject(AudioPath.CONVERSATION_DIR, get_name(AudioPath.CONVERSATION_DIR), output=PATH.OUTPUT_ROOT)
audio_source.apply_setting(TEST_SETTING)

# @pytest.mark.parametrize("test_payload", [audio_payload])
def test_con_dir():
    test_payload: ConversationDirectoryPayload = load_conversation_dir_payload(audio_source)[0]
    assert test_payload
    assert test_payload.name == get_name(AudioPath.CONVERSATION_DIR)
    logging.info(test_payload.original_source)
    logging.info(test_payload.setting.get_engine_setting())
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
    

def test_invalid_audio():
    paths = paths_in_dir(PATH.INVALID_DATA_DIR)
    paths.extend(subdirs_in_dir(PATH.INVALID_DATA_DIR))
    sources = [SourceObject(path, get_name(path), PATH.OUTPUT_ROOT) for path in paths]
    for source in sources:
        assert source
        assert source.name 
        assert not load_conversation_dir_payload(source)
        source.apply_setting(TEST_SETTING)
        assert not load_conversation_dir_payload(source)