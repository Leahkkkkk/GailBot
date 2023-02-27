from pydantic import BaseModel, ValidationError
from typing import Dict, List , Union
from .engineSettingInterface import EngineSettingInterface
# from gailbot.configs import interface_loader

# # INTERFACE_CONFIG = interface_loader()
# name = INTERFACE_CONFIG.watsonName

class InitSetting(BaseModel):
    apikey : str 
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
        setting = WatsonInterface(**setting)
        return setting
    except ValidationError as e:
        return False