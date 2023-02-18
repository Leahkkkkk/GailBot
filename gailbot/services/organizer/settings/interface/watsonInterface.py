from .settingInterface import EngineOption
from pydantic import BaseModel 
from typing import Dict, List 

class WatsonInterface(EngineOption):
    class watson_schema(BaseModel):
        pass 
    
    def __init__(self) -> None:
        raise NotImplementedError
   
    @staticmethod 
    def _is_valid(setting: Dict[str, str]) -> bool: 
        raise NotImplementedError
    
    def get_engine_name(self) -> str:
        return "Watson Engine"
    
        
    def get_setting_detail(self) -> Dict:
        raise NotImplementedError()