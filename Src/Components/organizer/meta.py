# Standard library imports 
from typing import Any
from enum import Enum
# Local imports 
from ...utils.models import IDictModel
# Third party imports 

class MetaAttributes(Enum):
    size = "size"
    number_of_files = "number_of_files"
    transcription_date = "transcription_date"
    transcriber_name = "transcriber_name"
    source_type = "source_type"
    previously_transcribed = "previously_transcribed"
    
class Meta(IDictModel):
    """
    Stores meta-data information about a whole conversation based on its 
    individual data files. 
    This is dependant on the data files. 
    """

    def __init__(self, data : Any) -> None:
        super().__init__(data)
        self.items = dict()
        for attribute in MetaAttributes:
            self.items[attribute] = None
        self.configured = self._parse_data(data)

    def _parse_data(self, data) -> bool:
        try:
            self.items[MetaAttributes.size] = data["size"]
            self.items[MetaAttributes.number_of_files] = data["number_of_files"]
            self.items[MetaAttributes.transcription_date] = \
                data["transcription_date"]
            self.items[MetaAttributes.transcriber_name] = \
                data["transcriber_name"]
            self.items[MetaAttributes.source_type] = data["source_type"]
            self.items[MetaAttributes.previously_transcribed] = \
                data["previously_transcribed"]
            return True 
        except:
            return False  
         