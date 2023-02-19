from typing import Dict
from .interface import EngineOption, WatsonInterface, GoogleInterface, WhisperInterface

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
    engine_setting: EngineOption   = None
    plugin_setting: PluginOption    = None 
    valid_interfaces = [WatsonInterface, GoogleInterface, WhisperInterface]
    
    # setting_path: str               = None NOTE: setting path will be provided by setting manager, so setting object does not need to know about it 
    # name: str                       = None NOTE: setting object only stores the data and not the name 
    
    def __init__(self, setting: Dict[str, str]) -> None:
        self.engine_setting = self._load_engine_setting(setting["engine"])
        self.plugin_setting = self._load_plugin_setting(setting["plugin"])
        
    def save_setting(self, output: str) -> bool: 
        raise NotImplementedError()
    
    def _load_plugin_setting(self, setting : Dict[str, str]) -> bool:
        raise NotImplementedError()

    def _load_engine_setting(self, setting : Dict[str, str]) -> bool:
        for option in self.valid_interfaces:
            set_obj = option(setting)
            if isinstance(set_obj, EngineOption):
                self.engine_setting = set_obj
                return True
        return False
      
    

