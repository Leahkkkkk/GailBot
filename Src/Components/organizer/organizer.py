# Standard library imports 
from typing import Tuple, List, Any
from copy import deepcopy
# Local imports 
from ..io import IO
from .builder import Builder
# Third party imports 

class Organizer:

    def __init__(self, io : IO) -> None:
        # Objects 
        self.builder = Builder(io)  
        self.conversations = list()

    def create_conversation(self, source_path : str, settings_profile : Any,
            transcriber_name : str) -> bool:

        is_successful =  self.builder.build_conversation(
            source_path, settings_profile ,transcriber_name) 
        if not is_successful:
            return False 
        self.conversations.append(self.builder.get_conversation())

    # TODO: Change return type from List[Any] to List[Conversation]
    def get_conversations(self) ->  List[Any]:
        return deepcopy(self.conversations)

    def clear_conversations(self) -> bool:
        self.conversations.clear()
        return True  
    



