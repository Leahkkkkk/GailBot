from tests.core.engines.data import AudioPath
from dataclasses import dataclass

WATSON_API_KEY         = "MSgOPTS9CvbADe49nEg4wm8_gxeRuf4FGUmlHS9QqAw3"
WATSON_LANG_CUSTOM_ID  = "41e54a38-2175-45f4-ac6a-1c11e42a2d54"
WATSON_REGION          = "dallas"
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
    WHISPER_SETTING = {
        "engine": "whisper", 
        "language": "English",
        "detect_speakers": False
    }

    GOOGLE_SETTING = {
        "engine": "google",
    }

    WATSON_SETTING = {
        "engine": "watson", 
        "api_key" : WATSON_API_KEY, 
        "region": WATSON_REGION,  
        "base_model": WATSON_BASE_LANG_MODEL,  
        "language_customization_id" : None,
        "acoustic_customization_id" : None
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

    WATSON_PROFILE = {
        "engine_setting": WATSON_SETTING,
        "plugin_setting": []
    }
    
    GOOGLE_PROFILE = {
        "engine_setting": GOOGLE_SETTING,
        "plugin_setting": []
    }

    WHISPER_PROFILE = {
        "engine_setting": WHISPER_SETTING,
        "plugin_setting": []
    }