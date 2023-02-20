from gailbot.services.organizer.settings import SettingManager
from gailbot.services.organizer.settings.interface import whisperInterface
from gailbot.core.utils.general import is_directory, is_file
import pytest


def test_setting_manager():
    manager = SettingManager()
    test_set = {"engine_setting": {"engine":"whisper"},
                "plugin_setting": ["hilab"]}
    
    manager.add_new_setting("test", test_set)
    
    # test create  and saving the profile
    manager.save_setting("test")
    assert manager.get_setting_names() == ["test"]
    for i in range(5):
        manager.add_new_setting(f"test{i}", test_set)
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
        manager.add_new_setting(old, test_set)
        assert manager.is_setting(old)
        assert is_file(manager.save_setting(old))
        manager.rename_setting(old, new)
        assert not manager.is_setting(old)
        assert manager.is_setting(new)
        assert is_file(manager.save_setting(new))
        

def test_init_and_load():
    manager = SettingManager()
    test_set = {"engine_setting": {"engine":"whisper"},
            "plugin_setting": ["hilab"]} 
    settings = [f"test{i}" for i in range(5)]
    for setting in settings:
        manager.add_new_setting(setting, test_set)
        manager.save_setting(setting)
    
    manager2 = SettingManager(load_exist=True)
    for setting in settings:
        assert manager2.is_setting(setting)
    
def test_setting_interface():
    suc_dict = {"engine": "whisper", "recognize_speaker": True}
    fail_dict = {"engine": "none", "recognizespeaker": True}
    res = whisperInterface.load_whisper_setting(suc_dict)
    print(res)
    assert not whisperInterface.load_whisper_setting(fail_dict)
    

