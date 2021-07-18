# Standard imports
from typing import Any
from abc import ABC, abstractmethod
# Local imports
from .blackboard import BlackBoard

class ConfigLoader(ABC):
    """
    Provides a template for any loaders to be used with Config.
    """

    def __init__(self) -> None:
        pass

    @abstractmethod
    def load_blackboard(self, blackboard_data : Any) -> BlackBoard:
        """
        Load the blackboard using the given data.

        Args:
            blackboard_data (Any)

        Returns:
            (Blackboard): Return None if the blackboard cannot be loaded.
        """
        pass