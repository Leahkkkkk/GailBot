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
from gailbot.configs import default_setting_loader
logger = makelogger("setting_object")

class EngineSetObj():
    """
    Store a single setting item 
    """
    engine_setting: EngineSettingInterface   = None
    name: str     = None                   
    valid_interfaces = [load_whisper_setting, load_google_setting, load_watson_setting] 
     
    def __init__(self, setting: Dict[str, str], name: str) -> None:
        self.name = name
        assert"engine_setting" in setting and "plugin_setting" in setting
        logger.info("initialize the setting object")
        assert self._load_engine_setting(setting)
        self.data = setting
        
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
        
    def get_setting_dict(self) -> Dict[str, str]:
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
            logger.error(e, exc_info=e)
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
       
        if self.engine_setting:
            self.data = setting
            return True
        else:
            return False
    
        
    def _load_engine_setting(self, setting : Dict[str, str]) -> bool:
        """
        Loads the engine settings

        Args:
            setting : List[str]: settings to load

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
        return False