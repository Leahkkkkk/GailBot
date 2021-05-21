# Standard library imports
from dataclasses import dataclass
# Local imports
from ....organizer import Conversation

@dataclass
class Source:
    conversation : Conversation

