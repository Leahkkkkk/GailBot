from pydantic import BaseModel, ValidationError
from typing import Any, Dict

class EngineSettingInterface(BaseModel):
    def __init__(__pydantic_self__, **data: Any) -> None:
        super().__init__(**data)
    
    def to_kwargs_dict(self) -> Dict[str, str] :
        """ convert the  engine setting data to kwargs dictionary 
            which can be directly used by stt engine    
        """
        d = self.dict()
        return d 