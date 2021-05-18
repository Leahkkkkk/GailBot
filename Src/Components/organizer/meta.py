# Standard library imports
from typing import Dict
from enum import Enum
# Local imports
from ...utils.models import IDictModel
# Third party imports

class MetaAttributes(Enum):
    """
    Inherits:
        (Enum)

    Attributes:
        conversation_name (str): Name of the conversation.
        total_size_bytes (bytes): Total size of all source files.
        num_data_files (int): Number of source files.
        source_type (str): Must be one of 'file' or 'directory'.
        transcription_date (datetime): Date the transcription process started.
        transcription_status (str): Status of the transcription.
        transcription_time (datetime): Time transcription process started.
        transcriber_name (str): Name of the transcriber
        num_speakers (int): Number of speakers in the conversation.
    """
    # General
    conversation_name = "conversation_name"
    total_size_bytes = "total_size_bytes"
    num_data_files = "num_data_files"
    source_type = "source_type"
    transcription_date = "transcription_date"
    transcription_status = "transcription_status"
    transcription_time = "transcription_time"
    transcriber_name = "transcriber_name"
    num_speakers = "num_speakers"

class Meta(IDictModel):

    def __init__(self, data : Dict[str,str]) -> None:
        """
        Args:
            data (Dict[str,Any]):
                Mapping from MetaAttributes as strings to their value.
        """
        super().__init__()
        self.configured = self._parse_data(data)

    def is_configured(self) -> bool:
        """
        Determine if the Paths object has successfully read data.

        Returns:
            (bool): True if data has been successfully read. False otherwise.
        """
        return self.configured

    def _parse_data(self, data : Dict[str,str]) -> bool:
        """
        Parse the given data into the model.

        Args:
            data (Dict[str,Any]):
                Mapping from DataFileAttributes as strings to their values.

        Returns:
            (bool): True if data has been successfully read. False otherwise.
        """
        try:
            if len(data.keys()) != len(MetaAttributes):
                return False
            for attr in MetaAttributes:
                self.items[attr] = data[attr.value]
            return True
        except:
            return False
