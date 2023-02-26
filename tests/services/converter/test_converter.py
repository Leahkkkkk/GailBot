import logging
from gailbot.services.converter import Converter 
from gailbot.services.organizer.settings import SettingObject
from gailbot.services.converter import PayLoadObject
from gailbot.services.organizer.source import SourceObject, SourceManager
from ..test_data import PATH, AudioPath, SETTING_DATA
from typing import List
from gailbot.core.utils.general import get_name, paths_in_dir

TEST_SETTING = SettingObject (SETTING_DATA.PROFILE, "test_setting")

def test_invalid_input():
    converter = Converter()    
    invalid_src = [SourceObject(p, get_name(p), PATH.OUTPUT_ROOT) for p in paths_in_dir(PATH.INVALID_DATA_DIR)]
    logging.info(invalid_src)
    payload_empty = converter(invalid_src)
    logging.info(payload_empty.__class__)
    logging.info(converter.payloads_dict)
    logging.info(payload_empty)
    assert len(payload_empty) == 0
    for source in invalid_src:
        source.apply_setting(TEST_SETTING)
    payload_empty = converter(invalid_src)
    assert len(payload_empty) == 0
    
def test_converter():
    paths = [PATH.TRANSCRIBED, AudioPath.MEDIUM_AUDIO, AudioPath.CONVERSATION_DIR]

    sources =[SourceObject(path, get_name(path), PATH.OUTPUT_ROOT) for path in paths]
    for source in sources:
        source.apply_setting(TEST_SETTING)

    test_converter = Converter()
    payloads: List[PayLoadObject] = test_converter(sources)
    for payload in payloads:
        logging.info(payload.__class__)
        logging.info(payload.data_files)
    assert len(payloads) == 3
    