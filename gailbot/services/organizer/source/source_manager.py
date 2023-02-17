from typing import List, Dict
from .source_object import Source
class SourceManager():
    """
    Holds and handles all functionality for managing all sources
    """
    def __init__(self) -> None:
        pass

    def remove_source(self) -> bool:
        raise NotImplementedError()
    
    def is_source(self, source_name:str) -> bool:
        raise NotImplementedError()

    def source_names(self) -> List[str]:
        raise NotImplementedError()

    def get_source(self, source_name:str) -> Source:
        raise NotImplementedError()

    def apply_setting_profile_to_source(self, setting_name:str, overwrite: bool):
        raise NotImplementedError()
    
    def get_sources_with_setting(self, setting_name:str): 
        raise NotImplementedError()
    
    def __repr__(self) -> str:
        raise NotImplementedError()