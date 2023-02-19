from typing import Dict
from .interface import EngineOption, WatsonInterface, GoogleInterface, WhisperInterface

""" NOTE: 
since the setting manager has the functionality to change the 
setting name, the setting object will not store the name of the 
setting, and all the setting name will be tracked and kept by
setting manager 
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
    setting_path: str               = None 
    name: str                       = None 
    valid_interfaces = [WatsonInterface, GoogleInterface, WhisperInterface]
    
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
      
    

