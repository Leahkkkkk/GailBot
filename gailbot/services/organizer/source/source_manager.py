from typing import List, Dict
from .source_object import SourceObject
from ..settings import SettingObject
from gailbot.core.utils.general import get_name
from gailbot.core.utils.logger import makelogger

logger = makelogger("source_manager")
class SourceManager():
    """
    Holds and handles all functionality for managing all sources
    """
    def __init__(self) -> None:
        self.sources : Dict[str, SourceObject] = dict()
    
    def add_source(self, source_path: str, output: str) -> bool:
        try:
            source  = SourceObject(source_path, name, output)
            name = source.get_source_name(get_name(source_path))
            self.sources[name] = source  
        except Exception as e:
            logger.error(e)
            return False
        else:
            return True
        
    def remove_source(self, source_name: str) -> bool:
        """
        Removes a given source from the source manager's sources

        Args:
            self
            source_name: str: name to remove

        Returns:
            True if given source was successfully removed, false if given source was not found
        """
        if not self.is_source(source_name):
            return False
        self.sources.pop(source_name)
        return True
    
    def is_source(self, source_name:str) -> bool:
        """
        Determines if a given source is currently in the source manager's sources

        Args:
            self
            source_name: str: key of the source to search for

        Returns:
            True if given source was found, false if not
        """
        if source_name in self.sources:
            return True
        else:
            return False


    def source_names(self) -> List[str]:
        """
        Obtains all source names as a list

        Args:
            self
        
        Returns:
            List of strings containing all source names
        """
        return list(self.sources.keys())

    def get_source(self, source_name:str) -> SourceObject:
        """
        Gets the source associated with a given source name

        Args:
            self
            source_name: str: string of name to search for
        
        Returns:
            Source object associated with the given name
            Raises exception if object with given name is not found
        """
        if self.is_source(source_name):
            return self.sources[source_name]
        else:
            return False

    def get_source_setting(self, source_name) -> SettingObject:
        if self.is_source(source_name):
            return self.sources[source_name].source_setting()
        else:
            return False

    def apply_setting_profile_to_source(self, source_name:str, setting: SettingObject, overwrite: bool):
        if self.is_source(source_name):
                self.sources[source_name].apply_setting(setting, overwrite)
                return self.sources[source_name].configured
        return False
    
    def get_sources_with_setting(self, setting_name:str) -> List[str]: 
        """
        Accesses all sources with a given settings profile

        Args:
            self
            setting_name: string of the settings profile to look for

        Returns:
            list of strings of all source names with the settings profile
        """
        return [k for k,v in self.sources.items() if v.setting.get_name() == setting_name]
    
    def is_source_configured(self, source_name:str) -> bool:
        """
        Determines if given source has been configured with settings

        Args:
            self
            source_name: string of the source name

        Returns:
            True if configured, false if not
        """
        return self.sources[source_name].configured
    
    def __repr__(self) -> str:
        return (f"Source manager with sources {self.source_names}")