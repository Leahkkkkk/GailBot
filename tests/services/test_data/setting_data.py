from tests.core.engines.data import AudioPath
from dataclasses import dataclass
""" 
test data 
setting: 
    engine setting - four at least, with different setting profiles, 
                     and one invalid profile
                     
    audio source - different length
    

"""
@dataclass 
class SETTING_DATA: 
    WHISPER_SETTING = {
        "engine": "whisper", 
        "transcribe": {
            "language": "English",
            "detect_speakers": False
        },
        "init": {}
    }

    GOOGLE_SETTING = {
        "engine": "google",
        "init": {},
        "transcribe": {}
    }


    PLUGIN_SETTING = ["hilab"]
    NEW_PLUGIN = ["testmodule"]
    
    # dummy profile for testing the organizer  & setting manager only 
    DUMMY_PROFILE = {
        "engine_setting": WHISPER_SETTING, 
        "plugin_setting": PLUGIN_SETTING
    }

    NEW_PROFILE = {
        "engine_setting": GOOGLE_SETTING, 
        "plugin_setting": NEW_PLUGIN
    }
    
    PROFILE = {
        "engine_setting": WHISPER_SETTING, 
        "plugin_setting": ["gb_test_suite"]
    }
    
    PROFILE_NO_PLUGIN = {
        "engine_setting": WHISPER_SETTING, 
        "plugin_setting": []
    }