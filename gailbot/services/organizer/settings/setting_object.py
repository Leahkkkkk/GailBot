from pydantic import BaseModel
from typing import Dict, List
from .interface import load_watson_setting, load_whisper_setting, load_google_setting
from gailbot.core.utils.logger import makelogger
from gailbot.core.utils.general import write_toml

logger = makelogger("setting_object")
""" NOTE: 
since the setting manager has the functionality to change the 
setting name, the setting object will not store the name of the 
setting, and all the setting name will be tracked and kept by
setting manager 

setting object only stores the setting data
"""
class PluginOption():
    """
    Provides an interface to validate plugin setting
    """
    def __init__(
        self,
        plugin: str) -> None:
        pass

    def is_valid_plugin(plugin_name:str) -> bool:
        raise NotImplementedError()

class SettingObject():
    """
    Store a single setting item 
    """
    engine_setting: BaseModel   = None
    plugin_setting: PluginOption    = None 
    name: str     = None                   
    valid_interfaces = [load_watson_setting, load_google_setting, load_whisper_setting] 
     
    def __init__(self, setting: Dict[str, str], name: str) -> None:
        self.data = setting
        self.engine_setting = self._load_engine_setting(setting["engine"])
        self.plugin_setting = self._load_plugin_setting(setting["plugin"])
        self.name = name
    

    def get_name(self):
        return self.name
    
    def change_profile_name(self, name):
        self.name = name 
        
    def save_setting(self, output: str) -> bool: 
        try:
            write_toml(output, self.data)
        except Exception as e:
            logger.error(e)
            return False
        else:
            return True
    
    def update_setting(self, setting: Dict[str, str]) -> bool:
        self.engine_setting = self._load_engine_setting(setting["engine"])
        self.plugin_setting = self._load_plugin_setting(setting["plugin"])
        if self.engine_setting and self.plugin_setting:
            return True
        else:
            return False
        
    def _load_plugin_setting(self, setting : List[str]) -> bool:
        self.plugin_setting = setting

    def _load_engine_setting(self, setting : Dict[str, str]) -> bool:
        for option in self.valid_interfaces:
            set_obj = option(setting)
            if isinstance(set_obj, BaseModel):
                self.engine_setting = set_obj
                return True
        return False
      
    

