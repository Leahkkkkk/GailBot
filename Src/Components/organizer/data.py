# Standard library imports
from typing import Any, Dict
from enum import Enum
# Local imports
from ...utils.models import IDictModel
# Third party imports

class DataFileTypes(Enum):
    """
    Defines the types of files that can be stored in DataFile objects.

    Inherits:
        (Enum)
    """
    audio = "audio"
    video = "video"

class DataFileAttributes(Enum):
    """
    Inherits:
        (Enum)

    Attributes:
        name (str): Name of the file
        extension (str): File extension
        path (str): Original path to the file.
        size_bytes (bytes): Size of the file.
        utterances (List[Utterance]):
            List of all utterances associated with this file.
    """
    name = "name"
    extension = "extension"
    file_type = "file_type"
    path = "path"
    size_bytes = "size_bytes"
    utterances = "utterances"


class DataFile(IDictModel):
    """
    Responsible for storing DataFileAttributes and their values.

    Inherits:
        (IDictModel)
    """
    def __init__(self, data : Dict[str,Any]) -> None:
        """
        Args:
            data (Dict[str,Any]):
                Mapping from DataFileAttributes as strings to their value.
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

    def set(self, attr : str, data : Any) -> bool:
        """
        Sets the given attribute to the data if it exists in the models attributes.

        Args:
            attr (Any)
            data (Any): Data associated with the attribute.

        Returns:
            (bool): true if successful. False otherwise.
        """
        # Explicit check for file_type attribute
        if attr == DataFileAttributes.file_type and \
                not isinstance(data,DataFileTypes):
            return False
        return super().set(attr,data)

    def _parse_data(self, data : Dict[str,Any]) -> bool:
        """
        Parse the given data into the model.

        Args:
            data (Dict[str,Any]):
                Mapping from DataFileAttributes as strings to their values.

        Returns:
            (bool): True if data has been successfully read. False otherwise.
        """
        try:
            for attr in DataFileAttributes:
                # Explicit check for file_type attribute
                if attr == DataFileAttributes.file_type and \
                        not isinstance(data[attr.value],DataFileTypes):
                    raise Exception
                self.items[attr] = data[attr.value]
            return True
        except:
            return False