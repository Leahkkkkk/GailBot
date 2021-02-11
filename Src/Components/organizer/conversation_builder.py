# Standard library imports 
from typing import Dict, Any, List 
from copy import deepcopy
# Local imports 
from ...utils.exceptions import ExceptionInvalid
from ..io import IO
from .conversation import Conversation
from .meta import Meta, MetaAttributes
from .data import DataFile,DataFileAttributes,DataFileTypes
from .settings import Settings
from .paths import Paths, PathsAttributes

# Third party imports 

class ConversationBuilder:

    def __init__(self, io : IO) -> None:
        # Params
        self.io = io 
        self.core_data = {
            "source_path" : None, 
            "conversation_name" : None,
            "transcription_status" : "ready",
            "total_speakers" : None,
            "result_dir_path" : None,
            "temp_dir_path" : None,
            "settings" : None }
        self.conversation = None

    ############################# PUBLIC METHODS #############################

    #### SETTERS

    def set_conversation_source_path(self, source_path : str) -> bool:
        """
        Set the path of the source from which the conversation is to be loaded,
        which can be a file or a directory.

        Args:
            source_path (str): Path to the source file or directory.

        Returns:
            (bool): True if successfully set. False otherwise.
        """
        if not self.io.is_directory(source_path) and \
                not self.io.is_file(source_path): 
            return False 
        self.core_data["source_path"] = source_path
        return True

    def set_conversation_name(self, name : str) -> bool:
        """
        Set the name for the conversation that is to be created. 
        The name simply acts as the unique identifier for the conversation.

        Args:
            name (str): Name for the conversation.
        
        Returns:
            (bool): True if successfully set. False otherwise.
        """
        self.core_data["conversation_name"] = name  

    def set_result_directory_path(self, result_dir_path : str) -> bool:
        """
        Path to the final result directory.
        The directory must either exist or the path must be valid. 

        Args:
            result_dir_path (str): Path to the final result 
        
        Returns:
            (bool): True if successfully set. False otherwise.
        """
        if not self.io.is_directory(result_dir_path) and \
                not self.io.create_directory(result_dir_path) and \
                not self.io.delete(result_dir_path):
            return False 
        self.core_data["result_dir_path"] = result_dir_path
        return True
    
            
    def set_temporary_directory_path(self, temp_dir_path : str) -> bool:
        """
        Path to the temporary workspace directory.
        The directory must either exist or the path must be valid. 

        Args:
            temp_dir_path (str): Path to the final result 
        
        Returns:
            (bool): True if successfully set. False otherwise.
        """
        if not self.io.is_directory(temp_dir_path) and \
                not self.io.create_directory(temp_dir_path) and \
                not self.io.delete(temp_dir_path):
            return False 
        self.core_data["temp_dir_path"] = temp_dir_path
        return True

    def set_number_of_speakers(self, num_speakers : int) -> bool:
        """
        Set the number of speakers that are part of this conversation.
        Must be at least 1.

        Args:
            num_speakers (int): Speakers part of the conversation.
        
        Returns:
            (bool): True if successfully set. False otherwise.
        """
        if num_speakers < 1:
            return False 
        self.core_data["total_speakers"] = num_speakers
        return True

    def set_conversation_settings(self, settings : Settings) -> bool:
        """
        Set the settings object for this conversation. 

        Args:
            settings (Settings)
        
        Returns:
            (bool): True if successfully set. False otherwise.
        """
        if not settings.is_configured():
            return False 
        self.core_data["settings"] = settings
        return True 
    
    ##### GETTERS

    # TODO: Determine if this needs to be implemented or not.
    # def get_conversation_configurations(self) -> Dict[str,Any]:
    #     return 

    def get_conversation(self) -> Conversation:
        return deepcopy(self.conversation)

    #### Others 

    def clear_conversation_configurations(self) -> bool:
        for k in self.core_data.keys():
            self.core_data[k] = None
        self.core_data["transcription_status"] = "ready"
        return True 

    def build_conversation(self) -> bool:
        if not self._is_ready_to_build():
            return False 
        # Create the data file objects first. 
        data_files = self._initialize_data_files()

        # Use datafile objects to initialize Meta values. 

    ############################# PRIVATE METHODS #############################

    def _is_ready_to_build(self) -> bool:
        return (all([v != None for v in self.core_data.values()])) 

    def _initialize_meta(self) -> Meta:
        pass 

    def _initialize_data_files(self) -> List[DataFile]:
        if self.io.is_file(self.core_data["source_path"]):
            pass 
        elif self.io.is_directory(self.core_data["source_path"]):
            pass 
        else:
            raise ExceptionInvalid

    def _initialize_data_file(self, source_file_path : str) -> DataFile:
        if not self.io.is_file(source_file_path):
            raise ExceptionInvalid 
        
    

    def _initialize_paths(self) -> Paths:
        pass 

    


