from pydantic import BaseModel, ValidationError
from typing import Dict, List 

class WhisperInterface(BaseModel):
    recognize_speaker      : bool
    language               : str


def load_whisper_setting(setting: Dict[str, str]):
    try:
        setting = WhisperInterface(**setting)
        return True
    except ValidationError as e:
        return False