from gailbot.services.controller import ServiceController
from gailbot.core.utils.general import is_file, paths_in_dir
from tests.core.engines.data import AudioPath as A
from gailbot.core.utils.general import get_name
import os
from gailbot.core.utils.logger import makelogger
from gailbot.core.utils.general import delete
from ..services.test_data import SETTING_DATA, PROFILE
logger = makelogger("test_controller")

TEST_SETTING = SETTING_DATA.PROFILE
UPDATED_SETTING = SETTING_DATA.NEW_PROFILE
SETTING_NAME = "test_setting"
NEW_SETTING = "new_setting"
SOURCES = [(A.LARGE_AUDIO_MP3, A.RESULT_OUTPUT), (A.MEDIUM_AUDIO, A.RESULT_OUTPUT),
           (A.TRANSCRIBED_DIR, A.RESULT_OUTPUT), [A.CONVERSATION_DIR, A.RESULT_OUTPUT]]


def test_controller():
    controller = ServiceController(False)
    logger.info(controller.organizer.setting_manager.workspace)
    controller.add_source(A.SMALL_AUDIO_MP3, A.RESULT_OUTPUT)
    assert controller.is_source(A.SMALL_AUDIO_MP3)
    assert controller.create_new_setting(SETTING_NAME, TEST_SETTING)
    logger.info (controller.save_setting(SETTING_NAME))
    assert controller.is_setting(SETTING_NAME)
    controller.rename_setting(SETTING_NAME, NEW_SETTING)
    controller.update_setting(NEW_SETTING, UPDATED_SETTING)
    assert not controller.is_setting(SETTING_NAME)
    assert controller.is_setting(NEW_SETTING)
    logger.info(controller.get_plugin_setting(NEW_SETTING))
    logger.info(controller.get_engine_setting(NEW_SETTING)) 
    assert controller.apply_setting_to_source(A.SMALL_AUDIO_MP3, NEW_SETTING)
    assert controller.add_sources(SOURCES)
    assert controller.apply_setting_to_sources(
        [src[0] for src in SOURCES], NEW_SETTING)
    sources = controller.organizer.get_configured_sources()
    logger.info(sources)
    payloads = controller.converter(sources)
    logger.info(payloads)
    controller.remove_source(get_name(A.SMALL_AUDIO_MP3))
    