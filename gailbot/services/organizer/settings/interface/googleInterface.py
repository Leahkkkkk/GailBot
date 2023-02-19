from pydantic import BaseModel, ValidationError
from typing import Dict, List 

class GoogleInterface(BaseModel):
    format: str
    

def load_google_setting(setting: Dict[str, str]):
    try:
        setting = GoogleInterface(**setting)
        return True
    except ValidationError as e:
        return False