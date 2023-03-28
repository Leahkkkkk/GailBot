import os 
from .payloadObject import PayLoadObject, PayLoadStatus
from ...organizer.source import SourceObject
from typing import List, Union
from gailbot.core.utils.general import (
    get_extension, 
    copy
)
""" NOTE: currently unused and not tested since gailbot does not support 
          for video transcription yet
"""
def load_video_payload(source: SourceObject) -> Union[bool, List(PayLoadObject)]:
    """
    Loads an instance of the video payload with a given source object
    """
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
        """
        Determines if a given file path has a supported file extension

        Args:
            file_path: str: name of the file path to check

        Returns:
            True if filepath is supported, false if not
        """
        return super().is_supported(file_path)

    def _copy_file(self) -> None:
        """
        Copies file to workspace
        """
        extension = get_extension(self.original_source)
        tgt_path =os.path.join(self.workspace.data_copy, f"{self.name},{extension}")
        copy(self.original_source, tgt_path)
        self.data_files = [tgt_path]
    
    def _set_initial_status(self) -> None:
        """
        Sets the initial status of the payload object to initialized
        """
        self.status = PayLoadStatus.INITIALIZED
        
    @staticmethod
    def supported_format() -> str:
        """
        Contains and accesses a list of the supported formats
        """
        """ TODO: add the format """
        return ["mp4"]
        
    def _convert_to_audio(self) -> bool:
        """
        Converts video file to audio file
        """
        raise NotImplementedError()

    def __repr__(self) -> str:
        return "Video payload"