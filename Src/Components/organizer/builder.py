# Standard library imports 
from typing import Tuple, Any, List
# Local imports 
from ..io import IO
from .conversation import Conversation
from .meta import Meta 
from .data import DataFile
# Third party imports 

class Builder:
    """
    Responsible for knowing how to build one Conversation object, which 
    is comprised of many sub-objects.
    """

    def __init__(self, io : IO) -> None:
        # Objects 
        self.io = io
        self.conversation = None

    # TODO: Change settings_profile to SettingsProfile
    def build_conversation(self, source_path : str, settings_profile : Any,
            transcriber_name : str) \
            -> bool:
        """
        Determine the type of conversation from files and build.
        """
        meta = self._create_meta(source_path, transcriber_name)
        data_files = self._create_data_files(source_path)
        self.conversation = Conversation(settings_profile, meta, data_files)
        return True

    # TODO: Change Any to Conversation
    def get_conversation(self) -> Conversation:
        """
        Obtain the previous conversation if it was successfully constructed.
        """
        return self.conversation

    ############################ PRIVATE METHODS ############################

    def _create_meta(self, source_path : str, transcriber_name : str) -> Meta:
        pass 

    def _create_data_files(self, source_path : str) -> List[DataFile]:
        pass 

    def _create_data_file(self) -> DataFile:
        pass
