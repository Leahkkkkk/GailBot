from typing import Dict, Union
from ..settings import SettingObject
from gailbot.core.utils.general import get_name

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
        self.output:str = output
        self.setting: SettingObject = None  

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
        if overwrite or not self.setting:
            self.setting = setting
    

    def __repr__(self) -> str:
        """
        Gets a message containing source details
        """
        return (f"Source object with name {self.name} and path {self.path}")