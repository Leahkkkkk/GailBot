from pydantic import BaseModel, ValidationError
from typing import Dict, List 

class WhisperInterface(BaseModel):
    engine: str = "whisper"
    recognize_speaker      : bool = False
    language               : str  = None
    


def load_whisper_setting(setting: Dict[str, str]):
    if setting["engine"] != "whisper" : return False
    try:
        setting = WhisperInterface(**setting)
        
        return setting
    except ValidationError as e:
        return False