from pydantic import BaseModel, ValidationError
from typing import Dict, List 
from .settingInterface import SettingInterface

class GoogleInterface(SettingInterface):
    engine: str = "google"
    format: str

def load_google_setting(setting: Dict[str, str]):
    if not setting["engine"] == "google": return False
    try:
        setting = GoogleInterface(**setting)
        return setting
    except ValidationError as e:
        return False
    