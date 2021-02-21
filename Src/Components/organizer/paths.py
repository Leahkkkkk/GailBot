# Standard library imports 
from typing import Dict
from enum import Enum
# Local imports 
from ...utils.models import IDictModel
# Third party imports

class PathsAttributes(Enum):
    """
    Inherits:
        (Enum)
    
    Attributes:
        result_dir_path (str): Path to the final output directory. 
        source_path (str): Path to the input file / directory.
        temp_dir_path (str): Path to a temporary directory unique to this 
                            conversations.
    """
    result_dir_path = "result_dir_path" 
    source_path = "source_path"
    temp_dir_path = "temp_dir_path"

class Paths(IDictModel):
    """
    Responsible for storing paths relevant to a conversation.

    Inheritance:
        (IDictModel)
    """

    def __init__(self, data : Dict[str,str]) -> None:
        """
        Args:
            data (Dict[str,str]):
                Mapping from path attributes as strings to their values. 
        """
        super().__init__()
        for attribute in PathsAttributes:
            self.items[attribute] = None
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
            data (Dict[str,str]):
                Mapping from path attributes as strings to their values. 
        
        Returns:
            (bool): True if data has been successfully read. False otherwise.
        """
        try:
            for attr in PathsAttributes:
                self.items[attr] = data[attr.value]
            return True 
        except:
            return False 








