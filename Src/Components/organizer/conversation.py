# Standard library imports 
from typing import Any, List
from enum import Enum
# Local imports 
from ...utils.models import IDictModel
from .meta import Meta
from .data import DataFile
# Third party imports 

class Conversation:
    """
    Model that can have multiple views.
    This needs to provide convenience functions for all internal objects 
    because nothing else should know what a conversation internally 
    consists of.
    Needs to provide convenience functions for everything.
    """

    # TODO: Change any to SettingsProfile
    def __init__(self, settings_profile : Any, meta_data : Meta, 
            data_files : List[DataFile] ) -> None:
        # Data objects part of Conversation.
        self.settings_profile = settings_profile 
        self.meta_data = meta_data
        self.data_files = data_files

    ################################ GETTERS ##################################

    #### Meta methods 
    def get_conversation_size(self) -> float:
        pass 
    
    def get_number_of_files(self) -> int:
        pass 

    def get_transcription_date(self) -> Any:
        pass 

    def get_transcriber_name(self) -> Any:
        pass 

    def get_source_type(self) -> str:
        pass 

    def was_previously_transcribed(self) -> bool:
        pass 

    #### DataFile methods 

    def get_data_file_names(self) -> List[str]:
        pass 

    def get_data_file_paths(self) -> List[str]:
        pass 

    def get_speaker_labels(self, data_file_name : str) -> List[str]:
        pass

    #### Settings data 

    #### 

    ################################ SETTERS #################################









