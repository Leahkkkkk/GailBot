from gailbot.services.organizer.settings import SettingManager
from gailbot.workspace import WorkspaceManager
from gailbot.services.organizer.settings.interface import whisperInterface
from gailbot.core.utils.general import is_directory, is_file, read_toml
from gailbot.core.utils.logger import makelogger 
from ...services.test_data.data import PROFILE, NEW_PROFILE
from ...services.test_data.path import PATH
from ...services.test_data.setting_data import SETTING_DATA
import logging 
from gailbot.core.utils.general import is_file
def test_engine_setting():
    manager = SettingManager(PATH.SETTING_ROOT)
    logging.info(manager.get_engine_setting_names())
    logging.info(manager.get_setting_names())
    
    ## test create and load new engine
    existing_setting = [SETTING_DATA.WHISPER_NAME, SETTING_DATA.WATSON_NAME, SETTING_DATA.GOOGLE_NAME, SETTING_DATA.WHISPER_SP_NAME]
    assert manager.add_new_engine(existing_setting[0], SETTING_DATA.WHISPER_SETTING, overwrite=True)
    assert manager.add_new_engine(existing_setting[1], SETTING_DATA.WATSON_SETTING, overwrite=True)
    assert manager.add_new_engine(existing_setting[2], SETTING_DATA.GOOGLE_SETTING, overwrite=True)
    assert manager.add_new_engine(existing_setting[3], SETTING_DATA.WHISPER_SPEAKER, overwrite=True)

    ## test create new setting 
    profile_names = ["whisper", "watson", "google"]
    assert manager.add_new_setting(profile_names[0], SETTING_DATA.WHISPER_PROFILE, overwrite=True)
    assert manager.add_new_setting(profile_names[1], SETTING_DATA.WATSON_PROFILE, overwrite=True)
    assert manager.add_new_setting(profile_names[2], SETTING_DATA.GOOGLE_PROFILE, overwrite=True)
   
    for profile in profile_names:
        assert manager.is_setting(profile) 
    
    
    dummpy_engine_setting_name = SETTING_DATA.DUMMPY_ENGINE_NAME
    ## test add engine setting  
    assert manager.add_new_engine(dummpy_engine_setting_name[0], SETTING_DATA.WHISPER_SPEAKER)
    assert manager.add_new_engine(dummpy_engine_setting_name[1], SETTING_DATA.WATSON_SETTING)
    assert manager.add_new_engine(dummpy_engine_setting_name[2], SETTING_DATA.GOOGLE_SETTING)
    
    for set in existing_setting:
        assert manager.is_engine_setting(set)
    
    for set in dummpy_engine_setting_name:
        assert is_file(manager.get_engine_setting_path(set))
        assert manager.is_engine_setting(set)
        
    ## test updating the engine setting to see if the profile setting will be updated 
    dummy_profile_names = SETTING_DATA.DUMMY_PROFILE_NAME
    assert manager.add_new_setting(dummy_profile_names[0], SETTING_DATA.DUMMY_PROFILE1)
    assert manager.add_new_setting(dummy_profile_names[1], SETTING_DATA.DUMMY_PROFILE2)
    assert manager.add_new_setting(dummy_profile_names[2], SETTING_DATA.DUMMY_PROFILE3)
    
    ## test update engine setting  
    for set in dummpy_engine_setting_name:
        assert manager.update_engine_setting(set, SETTING_DATA.WHISPER_SPEAKER)

    # test delete engine setting
    for set in dummpy_engine_setting_name:
        assert not manager.remove_engine_setting(set)
        
    for dummy_profile in dummy_profile_names:
        assert manager.remove_setting(dummy_profile)
    
    for set in dummpy_engine_setting_name:
        assert manager.remove_engine_setting(set)