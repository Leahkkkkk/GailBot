from .payloadObject import PayLoadObject, PayLoadStatus
from ...organizer.source import SourceObject
from typing import List, Dict 
from gailbot.core.utils.general import is_directory, subdirs_in_dir, paths_in_dir
from enum import Enum
from gailbot.core.utils.general import paths_in_dir, is_directory, get_name, get_extension, copy, subdirs_in_dir, is_file
from gailbot.core.utils.logger import makelogger
import os 

logger = makelogger("transcribed_dir_payload")

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
        # transcribed_result = self.transcription_result.read_result()
        # self.set_transcription_result(transcribed_result)
    
    @staticmethod
    def is_supported(file_path: str) -> bool:
        if not is_directory(file_path):
            logger.info("not valid diretcory ")
            return False 
        return is_file(os.path.join(file_path, ".gailbot"))
       
    def _copy_file(self) -> None:
        tgt_path = os.path.join(self.workspace.data_copy, f"{self.name}")
        copy(self.original_source, tgt_path)
        self.data_files = [tgt_path]
    
    def _set_initial_status(self) -> None:
        self.status = PayLoadStatus.TRANSCRIBED
    
    @property
    def supported_format(self) -> str:
        return "transcribed directory"