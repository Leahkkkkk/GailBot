from pydantic import BaseModel, ValidationError
from typing import Any, Dict

class EngineSettingInterface(BaseModel):
    engine: str 
    
    def get_init_kwargs(self) -> Dict[str, str]:
        d = self.dict()["init"]
        return d
    
    """ TODO. delete this """
    def to_kwargs_dict(self) -> Dict[str, str] :
        """ convert the  engine setting data to kwargs dictionary 
            which can be directly used by stt engine    
        """
        d = self.dict()["transcribe"]
        return d 
    
    def get_transcribe_kwargs(self) -> Dict[str, str] :
        """ convert the  engine setting data to kwargs dictionary 
            which can be directly used by stt engine    
        """
        d = self.dict()["transcribe"]
        return d
    
 