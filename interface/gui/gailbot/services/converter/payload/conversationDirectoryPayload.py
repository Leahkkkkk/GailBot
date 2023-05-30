import os 
from typing import List,  Union
from .payloadObject import PayLoadObject, PayLoadStatus
from ...organizer.source import SourceObject
from gailbot.core.utils.general import (
    paths_in_dir, 
    is_directory, 
    copy
)
from gailbot.core.utils.logger import makelogger
from gailbot.workspace.manager import WorkspaceManager
from .audioPayload import AudioPayload
from gailbot.core.utils.media import AudioHandler

MERGED_FILE_NAME = "merged"
logger = makelogger("conversation_payload")

def load_conversation_dir_payload(
    source: SourceObject, 
    ws_manager: WorkspaceManager
) -> Union [bool, List[PayLoadObject]]:
    """ Given a source object, convert it into an conversation directory payload 
        if the source stores a conversation directory
    
    Args:
        source (SourceObject): an instance of SourceObject that stores the 
        datafile and setting of the transcription

    Returns:
        Union[bool, List[PayLoadObject]]: return the converted payload if the 
        conversion is successful, return false other wise
    """
    original_source = source.source_path()
    if not is_directory(original_source) or not source.setting:
        return False
    if ConversationDirectoryPayload.is_supported(original_source):
        return [ConversationDirectoryPayload(source, ws_manager)]
   
    # NOTE: currently not support loading directory inside directory 
    return False
        

class ConversationDirectoryPayload(PayLoadObject):
    """ 
    Stores a conversation directory with only audio files 
    """
    def __init__(self, source: SourceObject, workspace: WorkspaceManager) -> None:
        super().__init__(source, workspace)
    
    @staticmethod 
    def supported_format() -> str:
        """
        Contains and accesses a list of the supported formats
        """
        return "directory"
        
    @staticmethod
    def is_supported(file_path: str) -> bool:
        """
        Determines if a given file path has a supported file extension

        Args:
            file_path: str: file path to check
        
        Returns: 
            bool: True if it contains a supported file extension, false if not
        """
        logger.info(file_path)
        if not is_directory(file_path):
            return False 
        sub_paths = paths_in_dir(file_path, AudioPayload.supported_format(), recursive=False)
        if len(sub_paths) == 0:
            return False
        return True
     
    def _copy_file(self) -> None:
        """
        Copies file to workspace
        """
        try:
            tgt_path = os.path.join(self.workspace.data_copy, f"{self.name}")
            copy(self.original_source, tgt_path)
            self.data_files = []
            sub_paths = paths_in_dir(tgt_path, AudioPayload.supported_format(), recursive=False)
            for path in sub_paths:
                self.data_files.append(path)
        except Exception as e:
            logger.error(e, exc_info=e)
    
    def _merge_audio(self):
        try:
            handler = AudioHandler()
            merged_path = handler.overlay_audios(self.data_files, self.out_dir.media_file, MERGED_FILE_NAME)
            self.merged_audio = merged_path
            assert merged_path
        except Exception as e:
            logger.error(e, exc_info=e)
    
    def _set_initial_status(self) -> None:
        """
        Sets the initial status of the payload object to initialized
        """
        self.status = PayLoadStatus.INITIALIZED

    def __repr__(self) -> str:
        return "Conversation directory payload"