from pydantic import BaseModel, ValidationError
from typing import Any, Dict

class EngineSettingInterface(BaseModel):
    engine: str 
    
    def get_init_kwargs(self) -> Dict[str, str]:
        """
            get the setting kwargs for initializing the engine
        """
        d = self.dict()["init"]
        return d
    
    def get_transcribe_kwargs(self) -> Dict[str, str] :
        """ 
            get the settings kwargs for transcribe function 
        """
        d = self.dict()["transcribe"]
        return d
    
 