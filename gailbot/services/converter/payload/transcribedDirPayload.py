from .payloadObject import PayLoadObject, PayLoadStatus
from ...organizer.source import SourceObject
from typing import List, Dict, Union
from gailbot.core.utils.general import is_directory, is_file, copy, paths_in_dir
from gailbot.core.utils.logger import makelogger
import os 

MAKER = "gailbot"
""" 
TODO by Feb 24
1. test function of loading the result file
"""
logger = makelogger("transcribed_dir_payload")

# TODO: ignore other file that is not audio files
def load_transcribed_dir_payload(source: SourceObject) -> Union[bool, PayLoadObject]:
    """
    Loads an instance of the transcribed directory payload with a 
        given source object
    """
    if not source.setting:
        return False
    if not TranscribedDirPayload.is_supported(source.source_path()):
        return False
    try: 
        return [TranscribedDirPayload(source)]
    except Exception as e:
        logger.error(e)
        return False

class TranscribedDirPayload(PayLoadObject):
    """
    Class for a transcribed directory payload
    """
    def __init__(self, source) -> None:
        super().__init__(source) 
        # find a better way to load result & get the result path
        if not self.transcription_result.load_result(
            os.path.join(self.data_files[0], "result/transcription")):
            self.status = PayLoadStatus.INITIALIZED
    
    @staticmethod
    def is_supported(file_path: str) -> bool:
        """
        Determines if a given file path has a supported file extension
        """
        if not is_directory(file_path):
            return False 
        return is_file(os.path.join(file_path, ".gailbot"))
       
    def _copy_file(self) -> None:
        """
        Copies file to workspace
        """
        tgt_path = os.path.join(self.workspace.data_copy, f"{self.name}")
        copy(self.original_source, tgt_path)
        self.data_files = [tgt_path]
    
    def _set_initial_status(self) -> None:
        """
        Sets the initial status of the payload object to initialized
        """
        self.status = PayLoadStatus.TRANSCRIBED
    
    @staticmethod
    def supported_format() -> str:
        """
        Contains and accesses a list of the supported formats
        """
        return "transcribed directory"

    def __repr__(self) -> str:
        return "Transcribed directory payload"