from pydantic import BaseModel, ValidationError
from typing import Any

class SettingInterface(BaseModel):
    engine: str 
    
    def __init__(__pydantic_self__, **data: Any) -> None:
        super().__init__(**data)
    
    def to_kwargs_dict(self):
        d = self.dict()
        d.pop("engine")
        return d 