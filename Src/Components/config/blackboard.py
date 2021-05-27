# Standard imports
from typing import Any, Dict
# Local imports
from .attributes import SystemBBAttributes
from ...utils.models import IDictModel
# Third party imports

class BlackBoard(IDictModel):
    """
    Generic BlackBoard class that must be inherited by all specific blackboard
    classes
    """
    def __init__(self, blackboard_data : Any) -> None:
        """
        Loads the given data into the blackboard if it can be correctly parsed.
        Every specific blackboard must have its function to parse the data

        Args:
            blackboard_data (Any): Data to be loaded into the blackboard
                        Must be in the format expected by the blackboard.
        """
        super().__init__()
        self.configured = False

    def is_configured(self) -> bool:
        """
        Determine if the blackboard is configured and ready for use.

        Returns:
            (bool): True if the blackboard is configured. False otherwise.
        """
        return self.configured

class SystemBB(BlackBoard):
    """
    The system blackboard is responsible for storing core system attributes.
    """

    def __init__(self, blackboard_data : Dict) -> None:
        """
        Args:
            blackboard_data (Dict):
                Data to be loaded into the blackboard. Must be a dictionary
                in the following format:
                {
                    "Test_key" : [Value for test key]
                }
        """
        super().__init__(blackboard_data)
        # Define the item dictionary.
        self.items = dict()
        for attribute in SystemBBAttributes:
            self.items[attribute] = None
        # Parse the blackboard data
        self.configured = self._parse_data(blackboard_data)

    ################################## PRIVATE METHODS #####################

    def _parse_data(self, blackboard_data : Dict) -> bool:
        """
        Parses the given data into the blackboard.

        Args:
            blackboard_data (Dict): Data to be parsed must be a dictionary

        Returns:
            (bool): True if successfully parsed. False otherwise.
        """
        try:
            for attr in SystemBBAttributes:
                self.items[attr] = blackboard_data[attr.value]
            return True
        except:
            return False

