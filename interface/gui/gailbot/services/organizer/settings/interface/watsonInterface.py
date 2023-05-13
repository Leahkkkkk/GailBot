from pydantic import BaseModel, ValidationError
from typing import Dict, Union
from .engineSettingInterface import EngineSettingInterface
from gailbot.core.utils.logger import makelogger
from gailbot.core.utils.download import is_internet_connected
from gailbot.core.engines import Watson
logger = makelogger("watson_interface")

class ValidateWatson(BaseModel):
    engine: str
    apikey : str 
    region: str 
    base_model: str 
    language_customization_id : str = None 
    acoustic_customization_id : str = None 

class InitSetting(BaseModel):
    apikey : str 
    region: str 
    
class TranscribeSetting(BaseModel):
    base_model: str 
    language_customization_id : str = None 
    acoustic_customization_id : str = None 
    
class WatsonInterface(EngineSettingInterface):
    """
    Interface for the Watson speech to text engine
    """
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
    if "engine" not in setting.keys() or setting["engine"] != "watson" or not is_internet_connected():
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
        watson_set["init"]["apikey"] = setting.pop("apikey")
        watson_set["init"]["region"] = setting.pop("region")
        watson_set["transcribe"].update(setting)
        logger.info(watson_set)
        watson_set = WatsonInterface(**watson_set)
        assert Watson.valid_init_kwargs(watson_set.init.apikey, watson_set.init.region)
        return watson_set
    except ValidationError as e:
        logger.error(e, exc_info=e)
        return False