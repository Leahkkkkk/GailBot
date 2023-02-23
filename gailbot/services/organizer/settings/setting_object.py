from typing import Dict, List
from .interface import (
    load_watson_setting, 
    load_whisper_setting, 
    load_google_setting, 
    EngineSettingInterface,
    PluginSettingsInterface
    )
from gailbot.core.utils.logger import makelogger
from gailbot.core.utils.general import write_toml

logger = makelogger("setting_object")



class SettingObject():
    """
    Store a single setting item 
    """
    engine_setting: EngineSettingInterface   = None
    plugin_setting: PluginSettingsInterface  = None 
    name: str     = None                   
    valid_interfaces = [load_watson_setting, load_google_setting, load_whisper_setting] 
     
    def __init__(self, setting: Dict[str, str], name: str) -> None:
        self.data = setting
        self._load_engine_setting(setting["engine_setting"])
        self._load_plugin_setting(setting["plugin_setting"])
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
        self._load_engine_setting(setting["engine_setting"])
        self._load_plugin_setting(setting["plugin_setting"])
        if self.engine_setting and self.plugin_setting:
            return True
        else:
            return False
    
    def _load_plugin_setting(self, setting : List[str]) -> bool:
        self.plugin_setting = PluginSettingsInterface(setting)

    def _load_engine_setting(self, setting : Dict[str, str]) -> bool:
        for option in self.valid_interfaces:
            set_obj = option(setting)
            if isinstance(set_obj, EngineSettingInterface):
                self.engine_setting = set_obj
                return True
        return False