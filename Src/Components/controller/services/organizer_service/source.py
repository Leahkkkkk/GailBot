# Standard library imports
from dataclasses import dataclass
# Local imports
from ....organizer import Conversation

@dataclass
class Source:
    source_name : str
    conversation : Conversation
    source_path : str
    settings_profile_name : str
    source_ws_path : str
    transcriber_name : str
    result_dir_path : str
    is_configured : bool