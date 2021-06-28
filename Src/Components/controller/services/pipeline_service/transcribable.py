# Standard imports
from dataclasses import dataclass,field
from typing import Dict
from ....engines import Utterance
from ....organizer import Conversation
# Local imports

@dataclass
class Transcribable:
    identifier : str
    conversation : Conversation
    source_status : Dict[str,bool] = field(default_factory=dict)
    source_to_transcribable_map : Dict[str,str] = field(default_factory=dict)
