from typing import Dict, List, Union, TypedDict, Optional
from .engineObject import EngineSetObj
from .pluginObject import PluginSuiteSetObj
from ..interface import (
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

class SettingDict(TypedDict):
    engine_setting_name: str
    plugin_setting: List[str]
    engine_setting: Optional[Dict[str, str]]

class SettingObject():
    """
    Store a single setting item 
    """
    engine_setting: EngineSetObj   = None
    plugin_setting: PluginSuiteSetObj  = None 
    name: str     = None                   
    valid_interfaces = [load_whisper_setting, load_google_setting, load_watson_setting] 
     
    def __init__(self, 
                 engine_setting_name:str, 
                 engine_setting: EngineSetObj ,
                 plugin_setting: PluginSuiteSetObj, name: str) -> None:
        self.name = name
        self.engine_setting_name = engine_setting_name
        self.engine_setting = engine_setting
        self.plugin_setting = plugin_setting
    
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
        
    def get_plugin_setting(self) -> List[str]:
        """
        Accesses and returns the object's plugin settings
        """
        return self.plugin_setting.get_data()
    
    def get_data(self) -> SettingDict:
        """
        Accesses and returns the object's setting dict
        """
        self.data = {"engine_setting": self.engine_setting.data, 
                     "engine_setting_name": self.engine_setting.name, 
                     "plugin_setting": self.plugin_setting.data}
        return self.data
    
    def save_setting(self, output: str) -> bool: 
        """
        Saves the settings to the output directory

        Args:
            output:str: output directory path

        Returns:
            bool: True if successfully saved, false if not
        """
        logger.info(output)
        try:
            write_toml(output, self.get_data())
        except Exception as e:
            logger.error(e, exc_info=e)
            return False
        else:
            return True
    
    def update_setting(self, engine_setting: EngineSetObj, plugin_setting: PluginSuiteSetObj) -> bool:
        """
        Updates the settings to a given dictionary

        Args: 
            setting: Dict[str, str]: new setting

        Returns:
            bool: True if successfully updated, false if not
        """
        try:
            logger.info(engine_setting)
            logger.info(plugin_setting)
            self.engine_setting.remove_applied_profile(self.name)
            self.engine_setting = engine_setting
            self.engine_setting.add_applied_profile(self.name)
            self.plugin_setting = plugin_setting
            assert self.get_data()
            return True
        except Exception as e:
            logger.error(e, exc_info=e)
            return False 