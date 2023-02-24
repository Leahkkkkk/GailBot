from .source import SourceObject, SourceManager
from gailbot.core.utils.logger import makelogger
from .settings import SettingManager, SettingObject
from typing import Dict, List
from gailbot.configs import path_config_loader, TemporaryFolder, OutputFolder
PATH_CONFIG = path_config_loader()
logger = makelogger("organizer")
class Organizer:
    workspace :str = PATH_CONFIG.gailbot_data.root
    def __init__(self, load_exist_setting: bool = False) -> None:
        self.setting_manager = SettingManager(load_exist_setting)
        self.source_manager  = SourceManager()
        
    def add_source(self, source_path: str, output: str) -> bool:
        return self.source_manager.add_source(source_path, output)
        
    def remove_source(self, source_name: str) -> bool:
        return self.source_manager.remove_source(source_name)
    
    def is_source(self, source_name: str) -> bool:
        return self.source_manager.is_source(source_name)
    
    def get_source(self, source_name: str) -> SourceObject:
        return self.source_manager.get_source(source_name)
    
    def get_source_setting(self, source_name: str) -> SettingObject:
        return self.source_manager.get_source_setting(source_name)
    
    def is_setting_applied(self, source_name: str) -> bool:
        return self.source_manager.is_source_configured(source_name)
    
    def apply_setting_to_source(self, source_name: str, setting_name:str, overwrite: bool = True) -> bool:
        return self.source_manager.apply_setting_profile_to_source(
            source_name, self.get_setting(setting_name), overwrite)

    def apply_setting_to_sources(self, sources: List[str], setting_name:str, overwrite: bool = True)-> bool:
        try:
            for source in sources:
                logger.info(source)
                assert self.apply_setting_to_source(source, setting_name, overwrite)
            return True
        except Exception as e:
            logger.error(e)
            return False
        
    def create_new_setting(self, setting_name: str, setting: Dict[str, str]) -> bool: 
        return self.setting_manager.add_new_setting(setting_name, setting)
    
    def save_setting_profile(self, setting_name: str) -> str:
        return self.setting_manager.save_setting(setting_name)
   
    """  add validation that all source's setting and disk file are changed accordingly"""
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
        self.setting_manager.update_setting(setting_name, new_setting)
        
    def get_setting(self, setting_name:str) -> SettingObject:
        return self.setting_manager.get_setting(setting_name)    

    def is_setting(self, setting_name: str) -> bool:
        return self.setting_manager.is_setting(setting_name)
    
    def remove_setting_from_source(self, source_name: str) -> bool:
        return self.source_manager.apply_setting_profile_to_source(source_name, None, True)
    
    def get_engine_setting(self, name: str):
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
    