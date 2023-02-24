from .payloadObject import PayLoadObject, PayLoadStatus
from ...organizer.source import SourceObject
from typing import List, Dict 
from gailbot.core.utils.general import is_directory, is_file, copy
from gailbot.core.utils.logger import makelogger
import os 

""" 
TODO by Feb 24
1. test function of loading the result file
"""
logger = makelogger("transcribed_dir_payload")

# TODO: ignore other file that is not audio files
def load_transcribed_dir_payload(source: SourceObject):
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
    def __init__(self, source) -> None:
        super().__init__(source) 
        if not self.transcription_result.load_result(
            os.path.join(self.workspace.data_copy, "result/transcription")):
            self.status = PayLoadStatus.INITIALIZED
    
    @staticmethod
    def is_supported(file_path: str) -> bool:
        if not is_directory(file_path):
            logger.info("not valid diretcory")
            return False 
        return is_file(os.path.join(file_path, ".gailbot"))
       
    def _copy_file(self) -> None:
        tgt_path = os.path.join(self.workspace.data_copy, f"{self.name}")
        copy(self.original_source, tgt_path)
        self.data_files = [tgt_path]
    
    def _set_initial_status(self) -> None:
        self.status = PayLoadStatus.TRANSCRIBED
    
    @staticmethod
    def supported_format() -> str:
        return "transcribed directory"