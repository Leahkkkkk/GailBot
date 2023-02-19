from typing import Dict
from ..settings import SettingObject
from gailbot.core.utils.general import get_name

class Source():
    """
    Holds and handles all functionality for a single source object
    """
    def __init__(self, path:str, name: str) -> None:
        self.source_name: str = name
        self.source_path: str = path
        self.setting: SettingObject = None  

    def source_details(self) -> Dict:
        """
        Accesses and returns the details about the given source.

        Args:
            self
        
        Returns:
            Dictionary containing the source name, source path, and settings profile
        """
        return {"source_name": self.source_name, 
                "source_path": self.source_path,
                "settings": self.setting }
    
    def source_path(self):
        return self.source_path

    def source_setting(self):
        return self.setting

    def setting_name(self) -> str:
        return self.setting.get_name()

    @property
    def configured(self) -> bool:
        """
        Determines if a given source was configured or not.

        Args:
            self

        Returns:
            Boolean representing whether or not the given source was configured
        """
        return self.setting != None
    
    def apply_setting(self, setting: SettingObject, overwrite: bool = True):
        if overwrite or not self.setting:
            self.setting = setting
    

    def __repr__(self) -> str:
        """
        Gets a message containing source details
        """
        return (f"Source object with name {self.source_name} and path {self.source_path}")