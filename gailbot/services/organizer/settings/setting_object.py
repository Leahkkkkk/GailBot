from typing import Dict
from abc import ABC

class EngineOption(ABC):
    """
    Provides an interface to validate setting 
             based on setting schema 
    """
    def __init__(self) -> None:
        pass

    def is_valid(setting : Dict [str, str]) -> bool:
        raise NotImplementedError()

    def setting_schema(self) -> Dict [str, str]:
        raise NotImplementedError()
    
    @property    
    def get_engine_name(self) -> str:
        raise NotImplementedError()

    @property
    def engine_detail(self) -> Dict:
        raise NotImplementedError()

class PluginOption():
    """
    Provides an interface to validate plugin setting
    """
    def __init__(
        self,
        plugin: str) -> None:
        pass

    def is_valid_plugin(plugin_name:str) -> bool:
        raise NotImplementedError()

class SettingObject():
    """
    Store a single setting item 
    """
    engine_setting : EngineOption 
    plugin_setting: PluginOption
    setting_path: str
    name: str
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    def load_setting(self, setting: Dict[str, str]) -> bool:
        raise NotImplementedError()
    
    def save_setting(self, output: str) -> bool: 
        raise NotImplementedError()
    
    def _load_engine_setting(self, setting : Dict[str, str]) -> bool:
        raise NotImplementedError()

    def _load_plugin_setting(self, setting : Dict[str, str]) -> bool:
        raise NotImplementedError()

    def update_setting(self, setting: Dict[str, str]) -> bool:
        raise NotImplementedError()

    def delete_setting(self) -> bool:
        raise NotImplementedError()

    def rename(self, name: str) -> None:
        raise NotImplementedError()
    
    

