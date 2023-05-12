from typing import Union
import os 

from .payloadObject import PayLoadObject, PayLoadStatus
from ...organizer.source import SourceObject
from gailbot.core.utils.general import is_directory, is_file, copy
from gailbot.core.utils.logger import makelogger
from gailbot.workspace.manager import WorkspaceManager
from gailbot.configs import service_config_loader, workspace_config_loader

HIDDEN_FILE = service_config_loader().directory_name.hidden_file
OUTPUT_RESULT = workspace_config_loader().get_output_structure().transcribe_result
logger = makelogger("transcribed_dir_payload")
MERGED_FILE_NAME = "merged"

def load_transcribed_dir_payload(
    source: SourceObject, ws_manager: WorkspaceManager) -> Union[bool, PayLoadObject]:
    """ given a source object, convert it into an PayloadObject  
        if the source stores a gailbot output directory that contains 
        the gailbot output result 
    
    Args:
        source (SourceObject): an instance of SourceObject that stores the 
        datafile and setting of the transcription

    Returns:
        Union[bool, List[PayLoadObject]]: return the converted payload if the 
        conversion is successful, return false other wise
    """
    if not source.setting:
        return False
    if not TranscribedDirPayload.is_supported(source.source_path()):
        return False
    try: 
        return [TranscribedDirPayload(source, ws_manager)]
    except Exception as e:
        logger.error(e, exc_info=e)
        return False

class TranscribedDirPayload(PayLoadObject):
    """
    Class for a transcribed directory payload
    """
    def __init__(self, source: SourceObject, ws_manager: WorkspaceManager) -> None:
        super().__init__(source, ws_manager) 
        if not self.transcription_result.load_result(
            os.path.join(self.data_files[0], OUTPUT_RESULT)):
            logger.error("result cannot be loaded")
            self.status = PayLoadStatus.INITIALIZED
    
    @staticmethod
    def is_supported(file_path: str) -> bool:
        """
        Determines if a given file path has a supported file extension

        Args:
            file_path: str: name of the file path to check

        Returns:
            bool: True if the file path is supported, false if not
        """
        if not is_directory(file_path):
            return False 
        return is_file(os.path.join(file_path, HIDDEN_FILE))
       
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
    
    def _merge_audio(self):
        try: 
            for root, dirs, files in os.walk(self.original_source):
                for file in files:
                    file_name, file_extension = os.path.splitext(file)
                    if file_name == MERGED_FILE_NAME:
                        logger.info(file)
                        merged_path = copy(os.path.join(root,file), self.out_dir.media_file)
                        self.merged_audio = merged_path
                        assert merged_path
                        break
        except Exception as e:
            logger.error(e, exc_info=e)
            return False
    
    @staticmethod
    def supported_format() -> str:
        """
        Contains and accesses a list of the supported formats
        """
        return "transcribed directory"

    def __repr__(self) -> str:
        return "Transcribed directory payload"