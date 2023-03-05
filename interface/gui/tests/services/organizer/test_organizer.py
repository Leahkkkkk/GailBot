from gailbot.services.organizer.organizer import Organizer 
from gailbot.core.utils.general import is_file
from tests.core.engines.data import AudioPath
from gailbot.core.utils.general import get_name
import os
from gailbot.core.utils.logger import makelogger
from ...services.test_data.data import PROFILE, NEW_PROFILE
from ...services.test_data import WS_MANGER
logger = makelogger("test_orgranizer")

TEST_SETTING =  PROFILE
UPDATED_SETTING = NEW_PROFILE

def test_construct_organizer():
    organizer = Organizer(WS_MANGER.setting_src)
    
#NOTE: get_source and is_source can be tested with other functions
def test_add_source():
    organizer = Organizer(WS_MANGER.setting_src)
    organizer.add_source(AudioPath.MEDIUM_AUDIO, AudioPath.GOOGLE_OUT_PATH)
    # logger.info(organizer.sour)
    assert organizer.is_source(get_name(AudioPath.MEDIUM_AUDIO))

def test_remove_source():
    organizer = Organizer(WS_MANGER.setting_src)
    organizer.add_source(AudioPath.MEDIUM_AUDIO, AudioPath.GOOGLE_OUT_PATH)
    assert organizer.is_source(get_name(AudioPath.MEDIUM_AUDIO))
    organizer.remove_source(get_name(AudioPath.MEDIUM_AUDIO))
    assert not organizer.is_source(get_name(AudioPath.MEDIUM_AUDIO))

def test_apply_setting():
    organizer = Organizer(WS_MANGER.setting_src)
    organizer.add_source(AudioPath.MEDIUM_AUDIO, AudioPath.GOOGLE_OUT_PATH)
    organizer.create_new_setting("test_setting", TEST_SETTING)
    organizer.apply_setting_to_source(get_name(AudioPath.MEDIUM_AUDIO), "test_setting")
    assert organizer.is_setting_applied(get_name(AudioPath.MEDIUM_AUDIO))
    assert organizer.get_source_setting(get_name(AudioPath.MEDIUM_AUDIO)).get_name() == "test_setting"

def test_remove_setting():
    organizer = Organizer(WS_MANGER.setting_src)
    setting = "test_setting"
    dummysource = [os.path.join(os.getcwd, f"dummy{i}") for i in range(10)]
    for dummy in dummysource:
        organizer.add_source(dummy, AudioPath.GOOGLE_OUT_PATH)
    
    organizer.create_new_setting(setting, TEST_SETTING)
    for dummy in dummysource:
        organizer.apply_setting_to_source(get_name(dummy), setting)
    organizer.remove_setting(setting)
    for dummy in dummysource:
        assert not organizer.is_setting_applied(dummy)
    
    
def test_change_setting():
    oldsetting = "old"
    newsetting = "new"
    organizer = Organizer(WS_MANGER.setting_src)
    organizer.create_new_setting(oldsetting, TEST_SETTING)
    
    dummysrc = [os.path.join(os.getcwd(), f"dummy{i}") for i in range(10)]
   
    for dummy in dummysrc:
        assert organizer.add_source(dummy, AudioPath.GOOGLE_OUT_PATH)
        assert organizer.apply_setting_to_source(get_name(dummy), oldsetting)
        assert organizer.get_source_setting(get_name(dummy)).name == oldsetting    
    
    organizer.rename_setting(oldsetting, newsetting)
    for dummy in dummysrc:
        assert organizer.get_source_setting(get_name(dummy)).name == newsetting


def test_create_and_save_setting():
    testnames = [f"test{i}" for i in range(10)]
    organizer = Organizer(WS_MANGER.setting_src)
    for name in testnames:
        organizer.create_new_setting(name, TEST_SETTING)
        assert organizer.is_setting(name)
        print(organizer.save_setting_profile(name))
        assert is_file(organizer.save_setting_profile(name))
         
    for name in testnames:
        organizer.remove_setting(name)
        assert not organizer.is_setting(name)
        assert not is_file(organizer.setting_manager.get_setting_path(name))

def test_update_setting():
    organizer = Organizer(WS_MANGER.setting_src)
    testnames = [f"test{i}" for i in range(10)]
    for name in testnames:
        organizer.create_new_setting(name, TEST_SETTING)
        organizer.update_setting(name, UPDATED_SETTING)
        assert organizer.get_setting(name)
        assert organizer.get_setting(name).plugin_setting.get_data() == UPDATED_SETTING["plugin_setting"]

def test_remove_setting():
    organizer = Organizer(WS_MANGER.setting_src)
    testnames = [f"test{i}" for i in range(5)]
    for name in testnames:
        organizer.create_new_setting(name, TEST_SETTING)
        path = organizer.save_setting_profile(name)
        assert is_file(path)
        organizer.remove_setting(name)
        assert not is_file(path)
        
    testname = "setting_to_delete"
    organizer.create_new_setting(testname, TEST_SETTING)
    sources = [
        AudioPath.MEDIUM_AUDIO, AudioPath.SMALL_AUDIO_MP3, AudioPath.LARGE_AUDIO_MP3, AudioPath.CONVERSATION_DIR]
    for source in sources:
        organizer.add_source(source, AudioPath.RESULT_OUTPUT)
        assert organizer.get_source_setting(source).name == "default"
    organizer.apply_setting_to_sources(sources, testname)
    for source in sources:
        assert organizer.get_source_setting(source).name == testname
    organizer.remove_setting(testname)
    for source in sources:
        assert organizer.get_source_setting(source).name == "default"
        
        