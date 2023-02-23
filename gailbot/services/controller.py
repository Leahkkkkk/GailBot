from typing import Dict, List, Any
from .organizer import Organizer 
from .converter import Converter 
""" Knows about all three sub modules """
class ServiceController:
    def __init__(self) -> None:
        self.organizer = Organizer()
        self.converter = Converter()
        
    
    def add_source(self, src_path: str, out_path: str) -> bool:
        return self.organizer.add_source(src_path, out_path)
        
    def remove_source(self, name: str) -> None:
        return self.organizer.remove_source(name)
    
    def is_source(self, name:str) -> None:
        return self.organizer.is_source(name)
    
    def create_new_setting(self, setting: Dict[str, str]) -> None:
        return self.organizer.create_new_setting(setting)
        
    def save_setting(self, setting_name: str) -> bool:
        raise self.organizer.save_setting_profile(setting_name)
    
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