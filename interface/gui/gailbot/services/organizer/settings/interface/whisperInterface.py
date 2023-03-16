from pydantic import BaseModel, ValidationError
from typing import Dict, List , Union
from .engineSettingInterface import EngineSettingInterface
from gailbot.core.utils.logger import makelogger

logger = makelogger("whisperInterface")
class ValidateWhisper(BaseModel): 
    engine              :str
    language            : str  = None
    detect_speakers     : bool = False
class Init(BaseModel): 
    pass
class TranscribeSetting(BaseModel):
    language            : str  = None
    detect_speakers     : bool = False
    
class WhisperInterface(EngineSettingInterface):
    """
    Interface for the Whisper speech to text engine
    """
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
    logger.info("initialize whisper engine")
    if  not "engine" in setting.keys() or setting["engine"] != "whisper": 
        return False
    try:
        logger.info(setting)
        setting = setting.copy()
        validate = ValidateWhisper(**setting)
        whisper_set = dict()
        whisper_set["engine"] = setting.pop("engine")
        whisper_set["init"] = dict()
        whisper_set["transcribe"] = dict()
        whisper_set["transcribe"].update(setting)
        whisper_set = WhisperInterface(**whisper_set)
        return whisper_set
    except ValidationError as e:
        logger.error(e, exc_info=e)
        logger.error(f"error in validating whisper interface {e}")
        return False