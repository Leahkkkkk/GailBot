# Standard imports
from typing import Dict, Any
from abc import ABC, abstractmethod

class Subscriber(ABC):

    @abstractmethod
    def handle(self, event_type : str, data : Dict[str,Any]) -> None:
        pass