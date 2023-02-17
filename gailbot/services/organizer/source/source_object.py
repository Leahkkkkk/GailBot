from typing import Dict
from ..settings import setting_object

class Source():
    """
    Holds and handles all functionality for a single source object
    """
    def __init__(self) -> None:
        source_name: str
        source_path: str
        settings: setting_object = None  

    def source_detail(self) -> Dict:
        raise NotImplementedError()
    
    def configured(self) -> bool:
        raise NotImplementedError()
    
    def apply_setting(self, setting: setting_object):
        raise NotADirectoryError()
    
    def __repr__(self) -> str:
        raise NotImplementedError()