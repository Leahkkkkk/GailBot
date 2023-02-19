from typing import Dict, Union, List
from .setting_object import SettingObject
import os
class SettingManager():
    """
    Manages all available settings 
    """
    settings : Dict[str , SettingObject]
    workspace: str
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    def get_setting_names(self) -> List[str]:
        return self.settings.keys()
    
    def remove_setting(name: str) -> bool:
        raise NotImplementedError()
    
    def get_setting(name:str) -> Dict[str, str]:
        raise NotImplementedError()

    def get_setting_path(name:str) -> str:
        raise NotImplementedError()

    def add_new_setting(self, name: str, path: str) -> str:
        raise NotImplementedError()

    def is_setting(self, name: str) -> bool:
        return name in self.get_setting_names()

    def update_setting(name: str, src: Union[str, dict]) -> bool:
        raise NotImplementedError()

    def rename_setting(name: str, new_name:str) ->bool:
        raise NotImplementedError()
    
    def save_setting(self, name:str) -> bool: 
        out_path = self._get_setting_path(name)
        self.settings[name].save_setting(out_path)    
    
    def _get_setting_path(self, name:str) -> str:
        return os.path.join(self.workspace, name + ".toml")