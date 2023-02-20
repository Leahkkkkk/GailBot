from gailbot.services.organizer.organizer import Organizer
from gailbot.core.utils.general import is_file
TEST_SETTING =  {"engine_setting": {"engine":"whisper"},
                "plugin_setting": ["hilab"]}

UPDATED_SETTING = {"engine_setting": {"engine":"whisper"},
                " plugin_setting": ["test_module"]}

def test_construct_organizer():
    organizer = Organizer()
    

#NOTE: get_source and is_source can be tested with other functions

def test_add_source():
    pass 

def test_remove_source():
    pass 

def test_is_setting_applied():
    pass 

def test_apply_setting():
    pass 

def test_remove_setting_from_source():
    pass 

def test_create_and_save_setting():
    testnames = [f"test{i}" for i in range(10)]
    organizer = Organizer()
    for name in testnames:
        organizer.create_new_setting(name, TEST_SETTING)
        assert organizer.is_setting(name)
        assert is_file(organizer.save_setting_profile(name))
        
        
    for name in testnames:
        organizer.remove_setting(name)
        assert not organizer.is_setting(name)
        assert not is_file(organizer.save_setting_profile(name))


def test_change_setting():
    pass 

def test_update_setting():
    organizer = Organizer()
    testnames = [f"test{i}" for i in range(10)]
    for name in testnames:
        organizer.add_source(name, TEST_SETTING)
        organizer.update_setting(name, UPDATED_SETTING)
        assert organizer.get_setting(name).plugin_setting == UPDATED_SETTING[" plugin_setting"]

def test_get_setting():
    pass 

def test_remove_setting():
    organizer = Organizer()
    testnames = [f"test{i}" for i in range(5)]
    for name in testnames:
        organizer.add_source(name, TEST_SETTING)
        path = organizer.save_setting_profile(name)
        assert is_file(path)
        organizer.remove_setting(name)
        assert not is_file(path)
