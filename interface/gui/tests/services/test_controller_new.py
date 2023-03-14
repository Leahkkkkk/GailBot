from gailbot.core.utils.logger import makelogger
from gailbot.services.controller import ServiceController
from tests.core.engines.data import AudioPath
from ..services.test_data import SETTING_DATA, PATH 
from tests.services.test_data.workspace import WS_MANAGER
import pytest 
logger = makelogger("test controller demo")

sources = [(AudioPath.FORTY_MIN, AudioPath.RESULT_OUTPUT), (AudioPath.LARGE_AUDIO_WAV, AudioPath.RESULT_OUTPUT), (AudioPath.LONG_PHONE_CALL, AudioPath.RESULT_OUTPUT), 
            (AudioPath.SHORT_PHONE_CALL, AudioPath.RESULT_OUTPUT)]

settings = [("watson test", SETTING_DATA.WATSON_SETTING), ("google test", SETTING_DATA.GOOGLE_SETTING), 
        ("whisper test", SETTING_DATA.WHISPER_SETTING), ("no plugin test", SETTING_DATA.PROFILE_NO_PLUGIN)]

updated_settings = []

@pytest.mark.parametrize("sources", sources)
@pytest.mark.parametrize("settings", settings)
def test_controller(sources, settings):
    controller = ServiceController(WS_MANAGER, False)
    controller.add_source(sources[0], sources[1])
    assert (controller.is_source(sources[0]))
    assert controller.create_new_setting(settings[0], settings[1])
    # test no duplicates
    assert not controller.create_new_setting(settings[0], settings[1])
    assert controller.is_setting(settings[0])

@pytest.mark.parametrize("settings", settings)
def test_update_setting(settings):
    controller = ServiceController(WS_MANAGER, False)
    controller.create_new_setting(settings[0], settings[1])


