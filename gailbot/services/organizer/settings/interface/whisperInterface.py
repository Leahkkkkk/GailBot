from pydantic import BaseModel, ValidationError
from typing import Dict, List 
from .settingInterface import SettingInterface

class WhisperInterface(SettingInterface):
    engine: str = "whisper"
    detect_speakers     : bool = False
    language               : str  = None
   
def load_whisper_setting(setting: Dict[str, str]):
    if setting["engine"] != "whisper" : return False
    try:
        setting = WhisperInterface(**setting)
        return setting
    except ValidationError as e:
        return False