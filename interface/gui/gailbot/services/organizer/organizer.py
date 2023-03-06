from .source import SourceObject, SourceManager
from gailbot.core.utils.logger import makelogger
from .settings import SettingManager, SettingObject, SettingDict
from typing import Dict, List, Union
from gailbot.configs import  TemporaryFolder, OutputFolder
logger = makelogger("organizer")
DEFAULT_SETTING_NAME = "default"

""" TODO: put this under toml file """
DEFAULT_SETTING = {
    "engine_setting": {
     "engine": "whisper",
     "transcribe": {
         "language": "English",
         "detect_speakers": False,
     },
     "init": {}
    },
    "plugin_setting": []
}

class Organizer:
    def __init__(self, setting_workspace: str, load_exist_setting: bool = False) -> None:
        self.setting_manager = SettingManager(setting_workspace, load_exist_setting)
        self.source_manager  = SourceManager()
        if not self.setting_manager.is_setting(DEFAULT_SETTING_NAME):
            self.setting_manager.add_new_setting(DEFAULT_SETTING_NAME, DEFAULT_SETTING)
        
    def add_source(self, source_path: str, output: str) -> bool:
        try:
            name = self.source_manager.add_source(source_path, output)
            assert name
            assert self.apply_setting_to_source(name, DEFAULT_SETTING_NAME)
            return True
        except Exception as e:
            logger.error(e)
            return False
        
    def remove_source(self, source_name: str) -> bool:
        return self.source_manager.remove_source(source_name)
    
    def is_source(self, source_name: str) -> bool:
        return self.source_manager.is_source(source_name)
    
    def get_source(self, source_name: str) -> Union [bool, SourceObject]:
        return self.source_manager.get_source(source_name)
    
    def get_source_setting(self, source_name: str) -> SettingObject:
        return self.source_manager.get_source_setting(source_name)
    
    def is_setting_applied(self, source_name: str) -> bool:
        return self.source_manager.is_source_configured(source_name)
    
    def apply_setting_to_source(
        self, source_name: str, setting_name:str, overwrite: bool = True) -> bool:
        return self.source_manager.apply_setting_profile_to_source(
            source_name, self.get_setting(setting_name), overwrite)

    def apply_setting_to_sources(
        self, sources: List[str], setting_name:str, overwrite: bool = True)-> bool:
        try:
            for source in sources:
                logger.info(source)
                assert self.apply_setting_to_source(source, setting_name, overwrite)
            return True
        except Exception as e:
            logger.error(e)
            return False
        
    def create_new_setting(
        self, setting_name: str, setting: Dict[str, str]) -> bool: 
        return self.setting_manager.add_new_setting(setting_name, setting)
    
    def save_setting_profile(self, setting_name: str) -> str:
        return self.setting_manager.save_setting(setting_name)
    
    def rename_setting(self, setting_name: str, new_name: str) -> bool:
        try:
            self.setting_manager.rename_setting(setting_name, new_name)
            return True
        except:
            return False
   
    def remove_setting(self, setting_name: str) -> bool:
        if not self.setting_manager.is_setting(setting_name):
            return False 
        
        self.setting_manager.remove_setting(setting_name)
        sources = self.source_manager.get_sources_with_setting(setting_name)
        
        for source in sources:
            self.remove_setting_from_source(source)
    
    def update_setting(self, setting_name:str, new_setting: Dict[str,str]) -> bool:
        return self.setting_manager.update_setting(setting_name, new_setting)
        
    def get_setting(self, setting_name:str) -> SettingObject:
        return self.setting_manager.get_setting(setting_name)    

    def get_setting_dict(self, setting_name:str) -> Union[bool, SettingDict]:
        return self.setting_manager.get_setting_dict(setting_name)

    def is_setting(self, setting_name: str) -> bool:
        return self.setting_manager.is_setting(setting_name)
    
    def remove_setting_from_source(self, source_name: str) -> bool:
        return self.apply_setting_to_source(
            source_name, DEFAULT_SETTING_NAME, True)
    
    def get_engine_setting(self, name: str) -> Union[bool, Dict[str, str]]:
        setting: SettingObject = self.setting_manager.get_setting(name)
        if setting:
            return setting.get_engine_setting()
        else:
            return False
        
    def get_plugin_setting(self, name: str):
        setting: SettingObject = self.setting_manager.get_setting(name)
        if setting:
            return setting.get_plugin_setting()
        else:
            return False
    
    def get_configured_sources(self, sources : List[str] = None) -> List[SourceObject]:
        return self.source_manager.get_configured_sources(sources)
    
    def remove_all_settings(self) -> bool:
        try:
            for setting in self.setting_manager.get_setting_names():
                if setting != DEFAULT_SETTING_NAME:
                    assert self.remove_setting(setting)

            for source in self.source_manager.get_configured_sources():
                assert source.setting_name() == DEFAULT_SETTING_NAME
            return True
        except Exception as e:
            logger.error(e)
            return False
    
    def get_setting_names(self) -> List[str]:
        return self.setting_manager.get_setting_names()
    
    def get_all_settings_data(self) -> Dict[str, SettingDict]:
        """ 
        return a dictionary that stores all setting data
        """
        return self.setting_manager.get_all_settings_data()