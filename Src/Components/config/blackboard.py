# Standard imports 
from typing import Any 
# Third party imports 
from enum import Enum

class BlackBoardAttributes(Enum):
    """
    Defines all the attributes that can exist within the blackboard
    """
    #TODO: Define the blackboard attributes
    pass 

class BlackBoard:

    def __init__(self) -> None:
        # Dictionary of the key-value pairs of items stored 
        self.items = {

        }

    def set(self, key : BlackBoardAttributes, data : Any) -> bool:
        """
        Sets the key with the provided data. The key must be a 
        BlackBoardAttribute 
        
        Args:
            key (BlackBoardAttributes)
            data (Any): Data to be associated with the key
            
        Returns:
            (bool): True if successful. False otherwise.
        """
        try:
            self.items[key] = data
            return True 
        except:
            return False 

    def get(self, key : BlackBoardAttributes) -> Any:
        """
        Get the value associated with the BlackBoardAttribute 
        
        Args:
            key (BlackBoardAttributes)
        
        Returns:
            data (Any): Data to be associated with the key
        """
        try:
            return self.items[key]
        except:
            pass 

    



