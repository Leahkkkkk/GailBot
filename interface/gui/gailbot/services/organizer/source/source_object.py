from typing import Dict, Union, Callable
from datetime import datetime
from ..settings import SettingObject
from gailbot.core.utils.logger import makelogger
from gailbot.configs import workspace_config_loader
import os
OUT_PUT_EXTENSION = workspace_config_loader().file_extension.output

logger = makelogger("source_object")
class SourceObject():
    name: str
    path: str
    output: str
    setting: SettingObject
    """
    Holds and handles all functionality for a single source object
    """
    def __init__(self, path:str, name: str, output: str) -> None:
        self.name: str = name
        self.path: str = path
        timestamp = datetime.now().strftime("_%m_%d_%y-%H-%M-%S")
        self.output:str = os.path.join(output, name + OUT_PUT_EXTENSION + timestamp)
        self.setting: SettingObject = None  
        self.progress_display: Callable = None 
        

    def source_details(self) -> Dict[str, Union[str, SettingObject]]:
        """
        Accesses and returns the details about the given source.
        
        Returns:
            Dictionary containing the source name, source path, and settings profile
        """
        return {"source_name": self.name, 
                "source_path": self.path,
                "settings": self.setting }
    
    def source_path(self):
        """
        Accesses the path of a source

        Returns:
            string containing the source path
        """
        return self.path

    def source_setting(self):
        """
        Accesses the source settings

        Returns:
            Settings object of the current source
        """
        return self.setting

    def setting_name(self) -> str:
        """
        Accesses the source name

        Returns:
            String name of the current source
        """
        return self.setting.get_name()

    def configured(self) -> bool:
        """
        Determines if a given source was configured or not.

        Returns:
            Boolean representing whether or not the given source was configured
        """
        return self.setting != None
    
    def apply_setting(self, setting: SettingObject, overwrite: bool = True):
        """
        Apply setting object

        Args:
            setting: SettingObject
            overwrite: bool

        Returns:
            None
        """
        logger.info(f"the setting object that is about to be applied is {setting}")
        if overwrite or not self.setting:
            self.setting = setting
            self.configured = True
    
    def add_progress_display(self, displayer: Callable):
        """ 
        Add a function to the source object that will take 
        in one string as argument
        

        Args:
            displayer (Callable): a function that will take in the string 
                                as a progress message 


        """
        if callable(displayer):
            self.progress_display = displayer
            return True 
        else:
            return False

    def __repr__(self) -> str:
        """
        Gets a message containing source details
        """
        return (f"Source object with name {self.name} and path {self.path}")