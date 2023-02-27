from pydantic import BaseModel, ValidationError
from typing import Dict, List , Union
from .engineSettingInterface import EngineSettingInterface

class Init(BaseModel): 
    pass
class TranscribeSetting(BaseModel):
    language            : str  = None
    detect_speakers     : bool = False
    
class WhisperInterface(EngineSettingInterface):
    transcribe : TranscribeSetting
    init: Init = None 
    engine: str 
   
def load_whisper_setting(setting: Dict[str, str]) -> Union[bool, EngineSettingInterface]:
    """ given a dictionary, load the dictionary as a whisper setting 

    Args:
        setting (Dict[str, str]): the dictionary that contains the setting data 

    Returns:
        Union[bool , SettingInterface]: if the setting dictionary is validated 
                                        by the whisper setting interface,
                                        return the google setting interface 
                                        as an instance of SettingInterface, 
                                        else return false
    """
    if  not "engine" in setting.keys() or setting["engine"] != "whisper": 
        return False
    try:
        setting = WhisperInterface(**setting)
        return setting
    except ValidationError as e:
        return False