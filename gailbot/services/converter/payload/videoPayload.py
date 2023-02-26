from .payloadObject import PayLoadObject, PayLoadStatus
from ...organizer.source import SourceObject
from typing import List, Dict, Union
from gailbot.core.utils.general import (
    get_extension, 
    copy)
import os 

def load_video_payload(source: SourceObject) -> Union[bool, List(PayLoadObject)]:
    if not source.setting:
        return False
    if not VideoPayload.is_supported(source.source_path):
        return False
    try:
        return [VideoPayload(source)]
    except:
        return False
class VideoPayload(PayLoadObject):
    def __init__(self, source) -> None:
        super().__init__(source)
    
    @staticmethod 
    def is_supported(file_path: str) -> bool:
        return super().is_supported()

    def _copy_file(self) -> None:
        extension = get_extension(self.original_source)
        tgt_path =os.path.join(self.workspace.data_copy, f"{self.name},{extension}")
        copy(self.original_source, tgt_path)
        self.data_files = [tgt_path]
    
    def _set_initial_status(self) -> None:
        self.status = PayLoadStatus.INITIALIZED
        
    @staticmethod
    def supported_format() -> str:
        """ TODO: add the format """
        return ["mp4"]
        
    def _convert_to_audio(self) -> bool:
        raise NotImplementedError()