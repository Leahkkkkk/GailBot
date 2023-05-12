from typing import List, Union
from .payloadObject import PayLoadObject, PayLoadStatus
from ...organizer.source import SourceObject
from gailbot.core.utils.general import (
    get_extension,  
    copy)
from gailbot.core.utils.logger import makelogger
from gailbot.core.utils.media import AudioHandler
import os 
from gailbot.workspace.manager import WorkspaceManager
from gailbot.configs import service_config_loader

SUPPORTED_AUDIO = service_config_loader().engines.audio_supported_format
MERGED_FILE_NAME = "merged"

logger = makelogger("audioPayload")

def load_audio_payload(
    source: SourceObject, ws_manager: WorkspaceManager) -> Union[bool, List[PayLoadObject]]:
    """ given a source object, convert it into an audio payload if the source 
    
    Args:
        source (SourceObject): an instance of SourceObject that stores the 
        datafile and setting of the transcription

    Returns:
        Union[bool, List[PayLoadObject]]: return the converted payload if the 
        conversion is successful, return false other wise
    """
    if not source.setting: 
        return False
    if not AudioPayload.is_supported(source.source_path()):
        return False  
    try:
        return [AudioPayload(source, ws_manager)]
    except Exception as e:
        logger.error(source.__class__)
        logger.error(e, exc_info=e)
        return False

class AudioPayload(PayLoadObject):  
    """
    Class for audio payload
    """
    def __init__(self, source: SourceObject, workspace: WorkspaceManager) -> None:
        super().__init__(source, workspace)
    
    @staticmethod
    def is_supported(file_path: str) -> bool:
        """
        Determines if a given file path has a supported file extension
        """
        logger.info(file_path)
        return get_extension(file_path) in SUPPORTED_AUDIO
    
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
        tgt_path =os.path.join(
            self.workspace.data_copy, f"{self.name}.{extension}")
        copy(self.original_source, tgt_path)
        self.data_files = [tgt_path]
        
    def _merge_audio(self):
        try:
            handler = AudioHandler()
            merged_path = handler.overlay_audios(self.data_files, self.out_dir.media_file, MERGED_FILE_NAME)
            self.merged_audio = merged_path
            assert merged_path
        except Exception as e:
            logger.error(e, exc_info=e)
            
    @staticmethod
    def supported_format() -> List[str]:
        """
        Contains and accesses a list of the supported formats
        """
        return SUPPORTED_AUDIO

    def __repr__(self) -> str:
        return "Audio payload"