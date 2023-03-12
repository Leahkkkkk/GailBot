from typing import Dict, List, Union, TypedDict
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


class SettingDict(TypedDict):
    engine_setting: Dict[str, str]
    plugin_setting: List[str]

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
        """
        Accesses and returns the object's name
        """
        return self.name
    
    def change_profile_name(self, name):
        """
        Changes the profile name to a given new name

        Args:
            name: name to change to
        """
        self.name = name 
        
    def get_engine_setting(self) -> Dict[str, str]:
        """
        Accesses and returns the object's engine settings
        """
        return self.engine_setting.to_kwargs_dict()
    
    def get_plugin_setting(self) -> List[str]:
        """
        Accesses and returns the object's plugin settings
        """
        return self.plugin_setting.get_data()
    
    def get_setting_dict(self) -> SettingDict:
        """
        Accesses and returns the object's setting dict
        """
        return self.data
    
    def save_setting(self, output: str) -> bool: 
        """
        Saves the settings to the output directory

        Args:
            output:str: output directory path

        Returns:
            bool: True if successfully saved, false if not
        """
        logger.info(self.data)
        try:
            write_toml(output, self.data)
        except Exception as e:
            logger.error(e)
            return False
        else:
            return True
    
    def update_setting(self, setting: Dict[str, str]) -> bool:
        """
        Updates the settings to a given dictionary

        Args: 
            setting: Dict[str, str]: new setting

        Returns:
            bool: True if successfully updated, false if not
        """
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
        """
        Loads the plugin settings

        Returns:
            bool: true if successfully loaded, false if not
        """
        logger.info("initialize plugin setting ")
        self.plugin_setting = PluginSettingsInterface(setting)

    def _load_engine_setting(self, setting : Dict[str, str]) -> bool:
        """
        Loads the engine settings

        Returns:
            bool: true if successfully loaded, false if not
        """
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