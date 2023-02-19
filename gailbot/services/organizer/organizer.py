
from .source import Source, SourceManager
from .settings import SettingManager
from typing import Dict
class Organizer:
    workspace :str = None # TODO: add a workspace
    
    def __init__(self) -> None:
        self.setting_manager = SettingManager()
        self.source_manager  = SourceManager()
        
    def add_source(self, source_name: str, source_path: str) -> bool:
        raise NotImplementedError()
    
    def remove_source(self, source_name: str) -> bool:
        return self.source_manager.remove_source(self, source_name)
    
    def is_source(self, source_name: str) -> bool:
        return self.source_manager.is_source(self, source_name)
    
    def get_source(self, source_name: str) -> Source:
        return self.source_manager.get_source(self, source_name)
    
    def is_setting_applied(self, source_name: str) -> bool:
        return self.source_manager.is_source_configured(source_name)
    
    def apply_setting_to_source(self, source_name: str, setting_name:str) -> bool:
        return self.source_manager.apply_setting_profile_to_source(
            source_name, self.get_setting(setting_name))
    
    def create_new_setting(self, setting_name: str, setting: Dict[str, str]) -> bool: 
        return self.setting_manager.add_new_setting(setting_name, setting)
    
    def save_setting_profile(self, setting_name: str) -> bool:
        return self.setting_manager.save_setting(setting_name)
   
    """  add validation that all source's setting and disk file are changed accordingly"""
    def change_setting_name(self, setting_name: str, new_name: str) -> bool:
        """ TODO: test  """
        # change on setting object 
        self.setting_manager.rename_setting(setting_name, new_name)
        raise NotImplementedError()
    
    def update_setting(self, setting_name:str, new_setting: Dict[str,str]) -> bool:
        self.setting_manager.update_setting(setting_name, new_setting)
        
    def is_setting(self, setting_name: str) -> bool:
        return self.setting_manager.is_setting(setting_name)
    
    def remove_setting_from_source(self, source_name: str) -> bool:
        return self.source_manager.apply_setting_profile_to_source(source_name, None, True)
    
    def get_setting(self, name: str):
        return self.setting_manager.get_setting(name)