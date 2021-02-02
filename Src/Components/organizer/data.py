# Standard library imports 
from typing import Any
from enum import Enum
# Local imports 
from ...utils.models import IDictModel
# Third party imports 

class DataFileAttributes(Enum):
    path = "path" 
    extension = "extension"
    name = "name"
    size = "size"
    speaker_labels = "speaker_labels"

class DataFile(IDictModel):
    """
    The data file can only be a supported type of file. 
    """

    def __init__(self, data : Any) -> None:
        super().__init__(data)
        self.items = dict()
        for attribute in DataFileAttributes:
            self.items[attribute] = None
        self.configured = self._parse_data(data)

    def _parse_data(self, data) -> bool:
        try:
            self.items[DataFileAttributes.path] = data["path"]
            self.items[DataFileAttributes.extension] = data["extension"]
            self.items[DataFileAttributes.name] = data["name"]
            self.items[DataFileAttributes.size] = data["size"]
            self.items[DataFileAttributes.speaker_labels] = \
                 data["speaker_labels"]
            return True 
        except:
            return False  



