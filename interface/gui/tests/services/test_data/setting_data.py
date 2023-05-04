from tests.core.engines.data import AudioPath
from dataclasses import dataclass

WATSON_API_KEY = "MSgOPTS9CvbADe49nEg4wm8_gxeRuf4FGUmlHS9QqAw3"
WATSON_LANG_CUSTOM_ID = "41e54a38-2175-45f4-ac6a-1c11e42a2d54"
WATSON_REGION = "dallas"
WATSON_BASE_LANG_MODEL = "en-US_NarrowbandModel"

""" 
test data 
setting: 
    engine setting - four at least, with different setting profiles, 
                     and one invalid profile
                     
    audio source - different length

"""


@dataclass
class SETTING_DATA:
    WHISPER_SP_NAME = "whisper speaker"
    WHISPER_SPEAKER = {
        "engine": "whisper",
        "language": "English",
        "detect_speakers": True,
    }

    WHISPER_NAME = "whisper"
    WHISPER_SETTING = {
        "engine": "whisper",
        "language": "English",
        "detect_speakers": False,
    }

    GOOGLE_NAME = "google"
    GOOGLE_SETTING = {
        "engine": "google",
        "google_api_key": "/Users/yike/Desktop/input/googleApi/gailbot_key.json",
    }

    WATSON_NAME = "watson"
    WATSON_SETTING = {
        "engine": "watson",
        "apikey": WATSON_API_KEY,
        "region": WATSON_REGION,
        "base_model": WATSON_BASE_LANG_MODEL,
        "language_customization_id": None,
        "acoustic_customization_id": None,
    }

    PLUGIN_SETTING = ["hilab"]
    NEW_PLUGIN = ["testmodule"]

    DUMMPY_ENGINE_NAME = ["engine1", "engine2", "engine3"]
    DUMMY_PROFILE_NAME = ["profile1", "profile2", "profile3"]
    # dummy profile for testing the organizer  & setting manager only

    DUMMY_PROFILE1 = {
        "engine_setting_name": DUMMPY_ENGINE_NAME[0],
        "plugin_setting": PLUGIN_SETTING,
    }

    DUMMY_PROFILE2 = {
        "engine_setting_name": DUMMPY_ENGINE_NAME[1],
        "plugin_setting": PLUGIN_SETTING,
    }

    DUMMY_PROFILE3 = {
        "engine_setting_name": DUMMPY_ENGINE_NAME[2],
        "plugin_setting": PLUGIN_SETTING,
    }
    PROFILE = {"engine_setting_name": WHISPER_SP_NAME, "plugin_setting": PLUGIN_SETTING}

    NEW_PROFILE = {"engine_setting_name": WHISPER_SP_NAME, "plugin_setting": NEW_PLUGIN}

    PROFILE_WITH_PLUGIN = {
        "engine_setting_name": WHISPER_SETTING,
        "plugin_setting": ["gb_hilab_suite"],
    }

    PROFILE_NO_PLUGIN = {"engine_setting_name": WHISPER_SETTING, "plugin_setting": []}

    WATSON_PROFILE = {
        "engine_setting_name": WATSON_NAME,
        "plugin_setting": ["gb_hilab_suite"],
    }

    GOOGLE_PROFILE = {
        "engine_setting_name": GOOGLE_NAME,
        "plugin_setting": ["gb_hilab_suite"],
    }

    WHISPER_SPEAKER_PROFILE = {
        "engine_setting_name": WHISPER_SP_NAME,
        "plugin_setting": ["gb_hilab_suite"],
    }

    WHISPER_PROFILE = {"engine_setting_name": WHISPER_NAME, "plugin_setting": []}
