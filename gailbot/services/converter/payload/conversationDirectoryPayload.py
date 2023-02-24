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
"""
logger = makelogger("conversation_payload")

def load_conversation_dir_payload(source: SourceObject) -> Union [bool, List[PayLoadObject]]:
    original_source = source.source_path()
    output = source.output
    setting = source.setting
    payloads = []
    
    if not is_directory(original_source):
        logger.error("not a directory")
        return False
    
    if ConversationDirectoryPayload.is_supported(original_source):
        return [ConversationDirectoryPayload(source)]
   
    # TODO: test recursively loading conversation
    sub_paths = paths_in_dir(original_source)
    for path in sub_paths:
        if is_directory(path):
            new_source = SourceObject(path, get_name(path), output)
            new_source.apply_setting(setting)
            new_payloads = load_conversation_dir_payload(new_source)
            if new_payloads:
                payloads.extend(new_payloads)
                
    return payloads
        
        

class ConversationDirectoryPayload(PayLoadObject):
    """ store a conversation directory with only audio files """
    def __init__(self, source) -> None:
        super().__init__(source)
    
    @property 
    def supported_format(self) -> str:
        return "directory"
        
    @staticmethod
    def is_supported(file_path: str) -> bool:
        """ NOTE: currently only support audio file  """
        if not is_directory(file_path):
            return False 
        sub_paths = paths_in_dir(file_path)
        for path in sub_paths:
            if not AudioPayload.is_supported(path):
                logger.warn("the directory contains files that cannot be\
                            processed by gailbot")
                return False
        return True
     
    def _copy_file(self) -> None:
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
        self.status = PayLoadStatus.INITIALIZED