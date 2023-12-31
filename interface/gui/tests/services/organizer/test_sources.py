from gailbot.services.organizer.source import SourceObject, SourceManager
from gailbot.services.organizer.settings import SettingObject

# from gailbot.configs.confs.toplevel import 
from gailbot.core.utils.general import get_name
from tests.core.engines.data import AudioPath

from gailbot.core.utils.logger import makelogger

logger = makelogger("test_organizer")

TEST_SETTING =  {"engine_setting": {"engine":"whisper"},
                "plugin_setting": ["hilab"]}

## test source object

def test_source_details():
    test_source = SourceObject(path= AudioPath.SMALL_AUDIO_MP3, name= "test", output= AudioPath.GOOGLE_OUT_PATH)
    details = test_source.source_details()
    assert(details["source_name"] == "test")
    assert(details["source_path"] == AudioPath.SMALL_AUDIO_MP3)
    # print(f"source_name: {details["source_name"]} , source_path: {details["source_path"]}, settings: {details["settings"]}" )
    #TODO print
    
def test_configured():
    test_source = SourceObject(path= AudioPath.SMALL_AUDIO_MP3, name= "test", output= AudioPath.GOOGLE_OUT_PATH)
    assert(not test_source.configured())
    test_source.apply_setting(TEST_SETTING, False)
    assert(test_source.configured())
    # assert(test_source.setting() == TEST_SETTING)

def test_apply_setting():
    test_source = SourceObject(path= AudioPath.SMALL_AUDIO_MP3, name= "test", output= AudioPath.GOOGLE_OUT_PATH)
    test_source.apply_setting(TEST_SETTING, False)
    assert(test_source.setting() == TEST_SETTING)


## test source manager

def test_get_source():
    test_source_manager = SourceManager()
    test_source_manager.add_source(AudioPath.SMALL_AUDIO_MP3, AudioPath.WATSON_OUT_PATH)
    name = get_name(AudioPath.SMALL_AUDIO_MP3)
    test_source = test_source_manager.get_source(name)

def test_remove_source():
    test_source_manager = SourceManager()
    test_source_manager.add_source(AudioPath.SMALL_AUDIO_MP3, AudioPath.WATSON_OUT_PATH)
    name = get_name(AudioPath.SMALL_AUDIO_MP3)
    test_source_manager.remove_source(name)
    assert(test_source_manager.is_source(name) == False)

def test_is_source():
    test_source_manager = SourceManager()
    test_source_manager.add_source(AudioPath.SMALL_AUDIO_MP3, AudioPath.WATSON_OUT_PATH)
    name = get_name(AudioPath.SMALL_AUDIO_MP3)
    assert(test_source_manager.is_source(name))

def test_source_names():
    test_source_manager = SourceManager()
    test_source_manager.add_source(AudioPath.SMALL_AUDIO_MP3, AudioPath.WATSON_OUT_PATH)
    test_source_manager.add_source(AudioPath.MEDIUM_AUDIO_MP3, AudioPath.WATSON_OUT_PATH)
    names = test_source_manager.source_names()
    for i in names:
        print(i)

def test_get_source():
    # implicitly tested
    pass

def test_apply_setting_profile_to_source():
    pass

def test_get_sources_with_setting():
    test_source_manager = SourceManager()
    setting = SettingObject(setting= ({"engine_setting": {"engine":"whisper"},
                "plugin_setting": ["hilab"]}), name= "test")
    test_source_manager.add_source(AudioPath.SMALL_AUDIO_MP3, AudioPath.WATSON_OUT_PATH)
    test_source_manager.apply_setting_profile_to_source(get_name(AudioPath.SMALL_AUDIO_MP3), setting, overwrite=False)
    test_source_manager.add_source(AudioPath.MEDIUM_AUDIO_MP3, AudioPath.WATSON_OUT_PATH)
    test_source_manager.apply_setting_profile_to_source(get_name(AudioPath.MEDIUM_AUDIO_MP3), setting, overwrite=False)
    results = test_source_manager.get_sources_with_setting("test")
    for i in results:
        print(i)
