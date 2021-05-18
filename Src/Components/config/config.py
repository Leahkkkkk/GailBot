# Standard imports
from typing import Tuple, Any
from copy import deepcopy
# Local imports
from .blackboard import BlackBoard,SystemBB
# Third party imports


class Config:
    """
    Responsible for managing different types of blackboards that store critical
    information.
    """
    def __init__(self) -> None:
        """
        Params:
            blackboards (Dict[str,BlackBoard]):
                Mapping from blackboard_type to a reference to the coresponding
                blackboard class.
            loaded_blackboards (Dict[str,BlackBoard]):
                Mapping from blackboard_type to an initialized object of the
                corresponding class.
        """
        self.blackboards = {
            "system_blackboard" : SystemBB}
        self.loaded_blackboards = dict()

    def load_blackboard(self, blackboard_type : str, blackboard_data : Any) \
            -> bool:
        """
        Load the given data into the blackboard of the specified type.
        The blackboard_type must be a defined type and the data must be
        in the format expected by the blackboard.
        Overwrites any existing blackboard of the same type.

        Args:
            blackboard_type (str): Type of the blackboard. Must be in the result
                                of method get_blackboard_types()
            blackboard_data (Any): Data to be parsed by the blackboard of the
                                specified type. Must be in the expected format.

        Returns:
            (bool): True if the blackboard was loaded correctly. False otherwise
        """
        # Check for type validity
        if not blackboard_type.lower() in self.blackboards.keys():
            return False
        #  Loading the appropriate blackboard, which is responsible for parsing
        # the data itself.
        blackboard_type = blackboard_type.lower()
        blackboard = self.blackboards[blackboard_type](blackboard_data)
        configured = blackboard.is_configured()
        if not configured:
            return False
        self.loaded_blackboards[blackboard_type] = blackboard
        return True

    def get_blackboard(self, blackboard_type : str) -> Tuple[bool,BlackBoard]:
        """
        Obtain a blackboard of the specified type that was previously loaded.
        The blackboard must have been previously loaded.

        Args:
            blackboard_type (str): Type of the blackboard. Must be in the result
                                of method get_blackboard_types()

        Returns:
            (Tuple[bool,Blackboard]): True + loaded blackboard if successful.
                                    False + None otherwise.
        """
        blackboard_type = blackboard_type.lower()
        if not blackboard_type in self.loaded_blackboards:
            return (False, None)
        return (True, deepcopy(self.loaded_blackboards[blackboard_type]))

    def get_blackboard_types(self) -> Tuple[str]:
        """
        Obtain a list of the supported blackboard_types.

        Returns:
            (Tuple[str]): List of supported blackboard types.
        """
        return tuple(self.blackboards.keys())
