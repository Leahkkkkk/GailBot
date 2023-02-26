from .payloadObject import PayLoadObject, PayLoadStatus
from ...organizer.source import SourceObject
from typing import List, Dict, Union
from gailbot.core.utils.general import (
    get_extension,  
    copy)
from gailbot.core.utils.logger import makelogger
import os 

logger = makelogger("audioPayload")

def load_audio_payload(source: SourceObject) -> Union[bool, List[PayLoadObject]]:
    if not source.setting: 
        return False
    if not AudioPayload.is_supported(source.source_path()):
        return False  
    # TODO: improve the logic of validating the format based on different engines
    try:
        return [AudioPayload(source)]
    except Exception as e:
        logger.error(source.__class__)
        logger.error(e)
        return False

class AudioPayload(PayLoadObject):  
    """
    Class for audio payload
    """
    def __init__(self, source: SourceObject) -> None:
       super().__init__(source) 
    
    @staticmethod
    def is_supported(file_path: str) -> bool:
        """
        Determines if a given file path has a supported file extension
        """
        logger.info(file_path)
        return get_extension(file_path) in ["mp3", "wav", "opus", "mpeg"] 
    
    def _set_initial_status(self) -> None:
        """
        Sets the initial status of the payload object to initialized
        """
        self.status = PayLoadStatus.INITIALIZED
    
    def _copy_file(self) -> None:
        """
        Copies file to workspace
        """
        extension = get_extension(self.original_source)
        tgt_path =os.path.join(self.workspace.data_copy, f"{self.name}.{extension}")
        copy(self.original_source, tgt_path)
        self.data_files = [tgt_path]
        
    @staticmethod
    def supported_format() -> List[str]:
        """
        Contains and accesses a list of the supported formats
        """
        return ["mp3", "wav", "opus", "mpeg"]

    def __repr__(self) -> str:
        return "Audio payload"