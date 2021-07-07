from dataclasses import dataclass
# Local imports
from ...organizer import Conversation
from .fs_service import SourceHook

@dataclass
class Source:
    source_name : str
    source_path : str
    result_dir_path : str
    hook : SourceHook
    transcriber_name : str
    settings_profile_name : str = None
    conversation : Conversation = None
    is_configured : bool = False

