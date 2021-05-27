# Standard library imports
from dataclasses import dataclass
# Local imports
from ....organizer import Conversation

@dataclass
class Source:
    conversation : Conversation
    source_name : str
    settings_profile_name : str
    source_ws_path : str

