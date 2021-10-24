# Standard imports
from typing import List, Any
# Local imports
from .blackboard import BlackBoard
from .loader import ConfigLoader


class Config:
    """
    Used to manage BlackBoard objects
    """

    def __init__(self) -> None:
        self.loaders: List[ConfigLoader] = list()

    ################################## MODIFIERS #############################

    def add_loader(self, config_loader: ConfigLoader) -> None:
        """
        Add a loader (or strategy) to load blackboards.
        """
        self.loaders.append(config_loader)

    def load_blackboard(self, blackboard_data: Any) -> BlackBoard:
        """
        Load a blackboard using the given data.
        Cycles through available strategies and uses the appropriate one to
        load the data.

        Raises:
             Exception if the blackboard is not loaded by any strategy.

        Args:
            blackboard_data (Any)

        Returns:
            (BlackBoard)
        """
        for loader in self.loaders:
            try:
                blackboard = loader.load_blackboard(blackboard_data)
                if blackboard != None:
                    return blackboard
            except:
                pass
        raise Exception("Blackboard data not loaded")

    ################################## GETTERS #############################

    def get_loaders(self) -> List[ConfigLoader]:
        """
        Obtain all the loaders.

        Returns:
            (List[ConfigLoader])
        """
        return self.loaders
