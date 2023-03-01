from gailbot.services.organizer.settings import SettingManager
from gailbot.workspace import WorkspaceManager
from gailbot.services.organizer.settings.interface import whisperInterface
from gailbot.core.utils.general import is_directory, is_file, read_toml
from gailbot.core.utils.logger import makelogger 
from ...services.test_data.data import PROFILE, NEW_PROFILE
import pytest
import random
from ...services.test_data import SETTING_DATA
from gailbot.services.organizer.settings.interface import load_google_setting, load_watson_setting, load_whisper_setting

logger = makelogger("test_setting_manager")

def test_setting_manager():
    manager = SettingManager(False)
    test_set = PROFILE
    
    manager.add_new_setting("test", test_set)
    
    # test create  and saving the profile
    manager.save_setting("test")
    assert manager.get_setting_names() == ["test"]
    
    for i in range(5):
        assert manager.add_new_setting(f"test{i}", test_set)
        path = manager.save_setting(f"test{i}")
        assert manager.is_setting(f"test{i}")
        assert is_file(path)
    
    # test remove the profile 
    assert manager.add_new_setting("test-delete", test_set)
    assert manager.save_setting("test-delete")
    manager.remove_setting("test-delete") 
    assert not manager.is_setting("test-delete")
    for i in range(5):
        manager.remove_setting(f"test{i}")
        assert not manager.is_setting(f"test{i}")
        assert not is_file(f"test{i}")

    #test rename interface 
    oldnames = [f"old_{i}" for i in range(5)]
    newnames = [f"new_{i}" for i in range(5)]
    
    for old, new in zip(oldnames, newnames):
        assert manager.add_new_setting(old, test_set)
        assert manager.is_setting(old)
        assert is_file(manager.save_setting(old))
        logger.info(manager.get_setting(old).engine_setting)
        manager.rename_setting(old, new)
        assert not manager.is_setting(old)
        assert manager.is_setting(new)
        assert is_file(manager.save_setting(new))
        logger.info(manager.get_setting(new).engine_setting)
        logger.info(manager.get_setting(new).plugin_setting)
    logger.info(manager.get_setting_names())
    logger.info(WorkspaceManager.get_setting_file())
    
    #test update profile
    for new in newnames:
        assert manager.update_setting(new, NEW_PROFILE)
        logger.info(manager.get_setting(new).get_engine_setting())
        logger.info(manager.get_setting(new).engine_setting.engine)
        assert (manager.get_setting(new).engine_setting.engine == "google") 
        logger.info(manager.get_setting(new).get_plugin_setting())
    for new_setting in WorkspaceManager.get_setting_file():
        logger.info(read_toml(new_setting))
    
    assert manager.delete_all_settings()
    
    
def test_init_and_load():
    manager = SettingManager()
    test_set = PROFILE
    settings = [f"test_2_{i}" for i in range(5)]
    for setting in settings:
        manager.add_new_setting(setting, test_set)
        manager.save_setting(setting)
    
    manager2 = SettingManager(load_exist=False)
    for setting in settings:
        assert manager2.is_setting(setting)
        logger.info(manager2.get_setting(setting).get_plugin_setting())        
        logger.info(manager2.get_setting(setting).get_engine_setting())        
    assert manager.delete_all_setting()
    assert manager2.delete_all_setting()
    
def test_setting_interface():
    suc_dict = {"engine": "whisper", "recognize_speaker": True}
    fail_dict = {"engine": "none", "recognizespeaker": True}
    res = whisperInterface.load_whisper_setting(suc_dict)
    print(res)
    assert not whisperInterface.load_whisper_setting(fail_dict)
    
def test_validate_setting():
    manager = SettingManager()
    assert manager.add_new_setting("whisper", SETTING_DATA.WHISPER_PROFILE)
    assert manager.add_new_setting("watson", SETTING_DATA.WATSON_PROFILE)
    assert manager.add_new_setting("google", SETTING_DATA.GOOGLE_PROFILE )
    