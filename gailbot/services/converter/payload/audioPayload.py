from .payloadObject import PayLoadObject, PayLoadStatus
from ...organizer.source import SourceObject
from typing import List, Dict, Union
from ...organizer import PATH_CONFIG, TemporaryFolder
from gailbot.core.utils.general import (
    get_extension, 
    get_name, 
    copy,
    write_toml, 
    write_json, 
    write_txt)
from gailbot.core.utils.logger import makelogger
import os 

logger = makelogger("audioPayload")

""" TODO: return the payload as a list """
def load_audio_payload(source: SourceObject) -> Union[bool, List[PayLoadObject]]:
    if not source.setting: 
        return False
    if not AudioPayload.is_supported(source.source_path()): 
        return False  
    # TODO: improve the logic of validating the format based on different engine
    try:
        return [AudioPayload(source)]
    except Exception as e:
        logger.error(e)
        return False

class AudioPayload(PayLoadObject):  
    def __init__(self, source: SourceObject) -> None:
       super().__init__(source) 
    
    @staticmethod
    def is_supported(file_path: str) -> bool:
        logger.info(file_path)
        return get_extension(file_path) in ["mp3", "wav", "opus"] 
    
    def _set_initial_status(self) -> None:
        self.status = PayLoadStatus.INITIALIZED
    
    def _copy_file(self) -> None:
        extension = get_extension(self.original_source)
        tgt_path =os.path.join(self.workspace.data_copy, f"{self.name}.{extension}")
        copy(self.original_source, tgt_path)
        self.data_files = [tgt_path]
        
    @property
    def supported_format(self) -> str:
        return ["mp3", "wav", "opus", "mpeg"]