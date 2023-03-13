from pydantic import BaseModel, ValidationError
from typing import Dict, List, Union
from .engineSettingInterface import EngineSettingInterface
from gailbot.core.utils.logger import makelogger

logger = makelogger("google_interface")
class ValidateGoogle(BaseModel):
    engine: str 
class Transcribe(BaseModel):
    """ 
    Args:
        BaseModel (_type_): _description_
    """
    pass 
class Init(BaseModel):
    pass 

class GoogleInterface(EngineSettingInterface):
    """
    Interface for the Google speech to text engine
    """
    init: Init = None 
    transcribe: Transcribe = None 
    engine: str 
    
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
        logger.error("not google")
        return False
    try:
        setting = setting.copy()
        validate = ValidateGoogle(**setting)
        setting["init"] = dict()
        setting["transcribe"] = dict()
        google_setting = GoogleInterface(**setting)
        return google_setting
    except ValidationError as e:
        logger.error(e)
        return False
