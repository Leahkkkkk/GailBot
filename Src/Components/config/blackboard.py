# Standard imports 
from typing import Any 
# Local imports 
from .attributes import BlackBoardAttributes


class BlackBoard:

    def __init__(self) -> None:
        # Dictionary of the key-value pairs of items stored 
        # Keys are only defined by BlackBoardAttributes 
        self.items = {}
        all_attrs = [v for v in BlackBoardAttributes]
        for attr in all_attrs:
            self.items[attr] = None 
    
    def set(self, key : BlackBoardAttributes, data : Any) -> bool:
        """
        Sets the key with the provided data. The key must be a 
        BlackBoardAttribute 
        
        Args:
            key (BlackBoardAttributes): Must be present in BlackBoardAttributes. 
            data (Any): Data to be associated with the key
            
        Returns:
            (bool): True if successful. False otherwise.
        """
        # The key must be present in BlackBoardAttributes 
        all_attrs = [v for v in BlackBoardAttributes]
        if key in all_attrs:
            self.items[key] = data
            return True 
        else:
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

    



