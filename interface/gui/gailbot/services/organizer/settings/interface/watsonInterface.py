from pydantic import BaseModel, ValidationError
from typing import Dict, List , Union
from .engineSettingInterface import EngineSettingInterface
from gailbot.core.utils.logger import makelogger
# from gailbot.configs import interface_loader


logger = makelogger("watson_interface")

# # INTERFACE_CONFIG = interface_loader()
# name = INTERFACE_CONFIG.watsonName
class ValidateWatson(BaseModel):
    engine: str
    api_key : str 
    region: str 
    base_model: str 
    language_customization_id : str = None 
    acoustic_customization_id : str = None 

class InitSetting(BaseModel):
    api_key : str 
    region: str 
    
class TranscribeSetting(BaseModel):
    base_model: str 
    language_customization_id : str = None 
    acoustic_customization_id : str = None 
    
class WatsonInterface(EngineSettingInterface):
    engine: str 
    init : InitSetting
    transcribe: TranscribeSetting
    
    @property
    def engine(self):
        return "watson"
    
def load_watson_setting(setting: Dict[str, str]) -> Union[bool, EngineSettingInterface]:
    """ given a dictionary, load the dictionary as a watson setting 

    Args:
        setting (Dict[str, str]): the dictionary that contains the setting data 

    Returns:
        Union[bool , SettingInterface]: if the setting dictionary is validated 
                                        by the watson setting interface,
                                        return the google setting interface 
                                        as an instance of SettingInterface, 
                                        else return false
    """ 
    if "engine" not in setting.keys() or setting["engine"] != "watson":
        return False
    try:
        logger.info(setting)
        setting = setting.copy()
        validate = ValidateWatson(**setting)
        logger.info(validate)
        watson_set = dict()
        watson_set["engine"] = setting.pop("engine")
        watson_set["init"] = dict()
        watson_set["transcribe"] = dict()
        watson_set["init"]["api_key"] = setting.pop("api_key")
        watson_set["init"]["region"] = setting.pop("region")
        watson_set["transcribe"].update(setting)
        logger.info(watson_set)
        watson_set = WatsonInterface(**watson_set)
        return watson_set
    except ValidationError as e:
        return False