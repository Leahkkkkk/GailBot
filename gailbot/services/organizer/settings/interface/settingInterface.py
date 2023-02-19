from abc import ABC 
from typing import Dict, List 
from pydantic import BaseModel

class EngineOption(ABC):
    """
    Provides an interface to validate setting 
             based on setting schema 
    """
    profile_schema : BaseModel = None  # subclass need to define this interface 
                                       # for validating the profile schema 
    
    def __init__(self) -> None:
        pass

    def is_valid(setting : Dict [str, str]) -> bool:
        raise NotImplementedError()

    @property
    def setting_schema(self) -> Dict [str, str]:
        raise NotImplementedError()
    
    @property    
    def get_engine_name(self) -> str:
        raise NotImplementedError()

    @property
    def get_setting_detail(self) -> Dict:
        raise NotImplementedError()
