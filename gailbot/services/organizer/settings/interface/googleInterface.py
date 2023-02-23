from pydantic import BaseModel, ValidationError
from typing import Dict, List, Union
from .engineSettingInterface import EngineSettingInterface

class GoogleInterface(EngineSettingInterface):
    format: str

def load_google_setting(setting: Dict[str, str]) -> Union[bool, EngineSettingInterface]:
    """ given a dictionary, load the dictionary as a google setting 

    Args:
        setting (Dict[str, str]): the dictionary that contains the setting data 

    Returns:
        Union[bool , SettingInterface]: if the setting dictionary is validated 
                                        by the google setting interface,
                                        return the google setting interface 
                                        as an instance of SettingInterface, 
                                        else return false
    """
    if not setting.pop("engine", "notfound") == "google": 
        return False
    try:
        setting = GoogleInterface(**setting)
        return setting
    except ValidationError as e:
        return False
    