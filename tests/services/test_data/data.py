from tests.core.engines.data import AudioPath
""" 
test data 
setting: 
    engine setting - four at least, with different setting profiles, 
                     and one invalid profile
                     
    audio source - different length
    

"""
WHISPER_SETTING = {
    "engine": "whisper", 
    "transcribe": {
        "language": "english",
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

PROFILE = {
    "engine_setting": WHISPER_SETTING, 
    "plugin_setting": PLUGIN_SETTING
}

NEW_PROFILE = {
    "engine_setting": GOOGLE_SETTING, 
    "plugin_setting": NEW_PLUGIN
}