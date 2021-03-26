# Standard library imports 
from typing import Dict, Any
from enum import Enum
# Local imports 
from ...utils.models import IDictModel
# Third party imports 

class UtteranceAttributes(Enum):
    """
    Defines the attributes of an utterance

    Attributes:
        speaker_label (str): Label associated with the speaker.
        start_time (float): Start time of the speaker in seconds.
        end_time (float): End time of the speaker in seconds.
        transcript (str): Text of the utterance
    """
    speaker_label = "speaker_label"
    start_time = "start_time"
    end_time = "end_time"
    transcript = "transcript"

class Utterance(IDictModel):
    """
    Object representing a single utterance in a conversation.

    Inherits:
        (IDictModel)
    """

    def __init__(self, data : Dict[str,Any]) -> None:
        """
        Params:
            data (Dict[str,str]): 
                Mapping from UtteranceAttribute string to its value. 
        """
        super().__init__()
        self.configured = self._parse_data(data)

    def is_configured(self) -> bool:
        """
        Determine if all the attributes of the utterance have values associated
        with them.

        Returns:
            (bool): True if configured. False otherwise.
        """
        return self.configured 

    def _parse_data(self, data : Dict[str,str]) -> bool:
        """
        Parse the data dictionary. 
        """
        try:
            if len(data.keys()) != len(UtteranceAttributes):
                return False 
            for attr in UtteranceAttributes:
                self.items[attr] = data[attr.value]
            return True 
        except:
            return False  


