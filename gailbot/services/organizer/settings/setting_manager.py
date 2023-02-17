from typing import Dict, Union
from .setting_object import SettingObject



class SettingManager():
    """
    Manages all available settings 
    """
    def __init__(self) -> None:
        settings : Dict[str , SettingObject]

    def remove_setting(name: str) -> bool:
        raise NotImplementedError()
    
    def get_setting(name:str) -> Dict[str, str]:
        raise NotImplementedError()

    def get_setting_path(name:str) -> str:
        raise NotImplementedError()

    def add_new_setting(name: str, path: str) -> str:
        raise NotImplementedError()

    def is_setting(name: str) -> bool:
        raise NotImplementedError()

    def update_setting(name: str, src: Union[str, dict]) -> bool:
        raise NotImplementedError()

    def rename_setting(name: str, new_name:str) ->bool:
        raise NotImplementedError()
    
    def save_setting(name:str) -> bool: 
        raise NotImplementedError()