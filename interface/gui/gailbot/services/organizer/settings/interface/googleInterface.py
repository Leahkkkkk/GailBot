import os
from pydantic import BaseModel, ValidationError
from typing import Dict, Union
from .engineSettingInterface import EngineSettingInterface
from gailbot.core.utils.logger import makelogger
from gailbot.core.engines.google import Google
from gailbot.core.utils.general import copy, is_file, is_directory, make_dir, get_name, get_extension
from gailbot.configs import  workspace_config_loader


API_KEY_DIR = workspace_config_loader().engine_ws.google_api

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
    # the path to a file that stores the google api key
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
        if not is_directory(API_KEY_DIR):
            make_dir(API_KEY_DIR)
        
        # check that the api key is valid
        assert Google.is_valid_google_api(setting["google_api_key"])
        
        # save a copied version of the api key file to the workspace
        copied_api = os.path.join(API_KEY_DIR, get_name(setting["google_api_key"]) + ".json")
        setting["google_api_key"] = copy(setting["google_api_key"], copied_api)
    
        google_set = dict ()
        google_set["engine"] = setting.pop("engine")
        google_set["init"] = dict()
        google_set["transcribe"] = dict()
        google_set["init"].update(setting)
        google_setting = GoogleInterface(**google_set)
        
        return google_setting
    except ValidationError as e:
        logger.error(e, exc_info=e)
        return False
