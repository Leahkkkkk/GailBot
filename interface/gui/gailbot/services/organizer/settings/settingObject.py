from typing import Dict, List, Union
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
DEFAULT_WHISPER_SETTING = {
    "engine": "whisper", 
    "language": "English", 
    "detect_speakers": False}

class SettingObject():
    """
    Store a single setting item 
    """
    engine_setting: EngineSettingInterface   = None
    plugin_setting: PluginSettingsInterface  = None 
    name: str     = None                   
    valid_interfaces = [load_whisper_setting, load_google_setting, load_watson_setting] 
     
    def __init__(self, setting: Dict[str, str], name: str) -> None:
        self.data = setting
        logger.info("initialize the setting object")
        self._load_engine_setting(setting["engine_setting"])
        self._load_plugin_setting(setting["plugin_setting"])
        self.name = name
    
    def get_name(self):
        return self.name
    
    def change_profile_name(self, name):
        self.name = name 
        
    def get_engine_setting(self) -> Dict[str, str]:
        return self.engine_setting.to_kwargs_dict()
    
    def get_plugin_setting(self) -> List[str]:
        return self.plugin_setting.get_data()
    
    def get_setting_dict(self) -> Dict[str, Union[str, Dict]]:
        return self.data
    
    def save_setting(self, output: str) -> bool: 
        logger.info(self.data)
        try:
            write_toml(output, self.data)
        except Exception as e:
            logger.error(e)
            return False
        else:
            return True
    
    def update_setting(self, setting: Dict[str, str]) -> bool:
        logger.info(setting)
        self._load_engine_setting(setting["engine_setting"])
        if "plugin_setting" in setting.keys():
            self._load_plugin_setting(setting["plugin_setting"])
        else:
            self._load_plugin_setting([])
            
        # NOTE: the plugin data is not required
        if self.engine_setting:
            self.data = setting
            return True
        else:
            return False
    
    def _load_plugin_setting(self, setting : List[str]) -> bool:
        logger.info("initialize plugin setting ")
        self.plugin_setting = PluginSettingsInterface(setting)

    def _load_engine_setting(self, setting : Dict[str, str]) -> bool:
        logger.info("initialize the engine setting")
        for option in self.valid_interfaces:
            logger.info(option)
            set_obj = option(setting)
            if isinstance(set_obj, EngineSettingInterface):
                self.engine_setting = set_obj
                return True
        logger.error(f"setting {setting} cannot be loaded, use default setting instead")
        self.engine_setting = load_whisper_setting(DEFAULT_WHISPER_SETTING)
        return True