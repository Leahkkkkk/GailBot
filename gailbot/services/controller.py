from typing import Dict, List, Any
""" Knows about all three sub modules """
class ServiceController:
    def __init__(self) -> None:
        raise NotImplementedError()
    
    def _init_workspace(self) -> None:
        raise NotImplementedError()
    
    def add_source(self, path: str) -> str:
        raise NotImplementedError() 
    
    def remove_source(self, name: str) -> None:
        raise NotImplementedError()
    
    def is_source(self, name:str) -> None:
        raise NotImplementedError()
    
    def create_new_setting(self, setting: Dict[str, str]) -> None:
        raise NotImplementedError()
    
    def save_setting(self, setting: Dict[str, str]) -> bool:
        raise NotImplementedError()
    
    def load_setting(self, path:str) -> bool:
        raise NotImplementedError()
    
    def rename_setting(self, profile: str, new_name: str) -> bool:
        raise NotImplementedError()
    
    def remove_setting(self, name: str) -> bool:
        raise NotImplementedError()
    
    def is_setting(self, name:str ) -> bool:
        raise NotImplementedError()
   
    def available_engine(self) -> List[str]:
        raise NotImplementedError()
    
    def transcribe(self) -> bool:
        raise NotImplementedError()
    
    def register_plugin_suite(self, suite_name, suite_path) -> str:
        raise NotImplementedError()
        
    def get_plugin_detail(self, suite_name) -> Dict[str, str]:
        raise NotImplementedError()
    
    def is_plugin(self, suite_name: str) -> bool:
        raise NotImplementedError()
    
    def delete_plugin(self, suite_name: str) -> bool:
        raise NotImplementedError()
    
    def apply_setting_to_sources(self, sources: List[str], setting: str) -> bool:
        raise NotImplementedError()
    
    def apply_setting_to_source(self, source: str, setting: str) -> bool:
        raise NotImplementedError()
    
    def check_source_status(self, source_name: str) -> str:
        raise NotImplementedError()