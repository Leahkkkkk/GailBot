from .payloadObject import PayLoadObject, PayLoadStatus
from ...organizer.source import SourceObject
from gailbot.core.utils.general import paths_in_dir, is_directory, get_name, get_extension, copy
from gailbot.core.utils.logger import makelogger
from .audioPayload import load_audio_payload, AudioPayload
import os 
from typing import List, Dict, Union

""" TODO:
1. test directory with different content
2. test directory with large file
3. change the load directory only loading audio file  
"""
logger = makelogger("conversation_payload")

def load_conversation_dir_payload(source: SourceObject) -> Union [bool, List[PayLoadObject]]:
    """ given a source object, convert it into an conversation directory payload 
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
        return [ConversationDirectoryPayload(source)]
   
    # NOTE: currently not support loading directory inside directory
    # sub_paths = paths_in_dir(original_source)
    # output = source.output
    # setting = source.setting
    # payloads = []
    # for path in sub_paths:
    #     if is_directory(path):
    #         new_source = SourceObject(path, get_name(path), output)
    #         new_source.apply_setting(setting)
    #         new_payloads = load_conversation_dir_payload(new_source)
    #         if new_payloads:
    #             payloads.extend(new_payloads)
                
    return False
        

class ConversationDirectoryPayload(PayLoadObject):
    """ 
    Stores a conversation directory with only audio files 
    """
    def __init__(self, source) -> None:
        super().__init__(source)
    
    @staticmethod 
    def supported_format() -> str:
        """
        Contains and accesses a list of the supported formats
        """
        return "directory"
        
    @staticmethod
    def is_supported(file_path: str) -> bool:
        """ NOTE: currently only support audio file  """
        """
        Determines if a given file path has a supported file extension
        """
        logger.info(file_path)
        if not is_directory(file_path):
            return False 
        sub_paths = paths_in_dir(file_path, AudioPayload.supported_format())
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
            sub_paths = paths_in_dir(tgt_path)
            for path in sub_paths:
                self.data_files.append(path)
        except Exception as e:
            logger.error(e)
    
    def _set_initial_status(self) -> None:
        """
        Sets the initial status of the payload object to initialized
        """
        self.status = PayLoadStatus.INITIALIZED

    def __repr__(self) -> str:
        return "Conversation directory payload"