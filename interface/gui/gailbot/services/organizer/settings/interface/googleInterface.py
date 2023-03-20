from pydantic import BaseModel, ValidationError
from typing import Dict, Union
from .engineSettingInterface import EngineSettingInterface
from gailbot.core.utils.logger import makelogger
from gailbot.core.engines.google import Google

logger = makelogger("google_interface")
class ValidateGoogle(BaseModel):
    engine: str 
    google_api_key: str
class Transcribe(BaseModel):
    """ 
    NOTE: google does not support additional kwargs in transcription
    """
    pass 
class Init(BaseModel):
    google_api_key: str 

class GoogleInterface(EngineSettingInterface):
    """
    Interface for the Google speech to text engine
    """
    engine: str 
    init: Init = None 
    transcribe: Transcribe = None 
    
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
    logger.info(setting)
    if  not "engine" in setting.keys() or setting["engine"] != "google": 
        return False
    try:
        setting = setting.copy()
        validate = ValidateGoogle(**setting)
        google_set = dict ()
        google_set["engine"] = setting.pop("engine")
        google_set["init"] = dict()
        google_set["transcribe"] = dict()
        google_set["init"].update(setting)
        google_setting = GoogleInterface(**google_set)
        assert Google.is_valid_google_api(google_setting.init.google_api_key)
        return google_setting
    except ValidationError as e:
        logger.error(e, exc_info=e)
        return False
