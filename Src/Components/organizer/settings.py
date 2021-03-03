# Standard library imports 
from typing import Any, Dict, List, Tuple
from enum import Enum
from copy import deepcopy 
# Local imports 
from ...utils.models import IDictModel
# Third party imports 

# TODO: Add actual settings attributes when finalized
class SettingsAttributes(Enum):
    sample_attribute_1 = "sample_attribute_1"
    sample_attribute_2 = "sample_attribute_2"

class Settings(IDictModel):
    """
    Responsible for storing SettingsAttributes and their values 

    Inherits:
        (IDictModel)
    """
    
    def __init__(self, data : Dict[str,str]) -> None:
        """
        Args:
            data (Dict[str,str]): 
                Mapping from SettingsAttributes string values to their 
                actual values
        """
        super().__init__()
        self.configured = self._parse_data(data)

    def is_configured(self) -> bool:
        """
        Determine if the Paths object has successfully read data. 

        Returns:
            (bool): True if data has been successfully read. False otherwise.
        """
        return self.configured 

    def set(self, attr : str, data : Any) -> bool:
        """
        No Setting attribute can be manually changed.

        Args:
            attr (str): Attribute to change
            data (Any): Data to be set as the value for that attribute 

        Returns:
            (bool): Always returns False. 
        """
        return False  

    def _parse_data(self, data : Dict[str,str]) -> bool:
        """
        Maps the key-value pairs in the data object into the internal 
        representation. data must contain all keys in SettingsAttributes. 

        Args:
            data (Dict[str,str]): 
                Mapping from SettingsAttributes string values to their actual
                values.

        Returns:
            (bool): True if successfully parsed. False otherwise. 
        """
        try:
            for attr in SettingsAttributes:
                self.items[attr] = data[attr.value]
            return True 
        except:
            return False 
        
class SettingsBuilder:
    """
    Responsible for constructing and performing different operations on 
    Settings objects. 
    """
    def __init__(self) -> None:
        pass 

    def create_settings(self, data : Dict[str,str]) -> Tuple[bool,Settings]:
        """
        Generate a Settings object from the provided data. 
        The data must only contain SettingsAttributes as keys and their
        associated values. 

        Args:
            data (Dict[str,str]): 
                Mapping from SettingsAttributes string values to their 
                actual values
        
        Returns:
            (Tuple[bool,Settings]):
                True + Settings object if successful.
                False + None if unsuccessful. 
        """
        all_attribute_values = \
            [attribute.value for attribute in list(SettingsAttributes)]
        if len(all_attribute_values) != len(data.keys()) or \
                not self._contains_keys(data, all_attribute_values):
            return (False, None)
        settings = Settings(data)
        if not settings.is_configured():
            return (False, None)
        return (True, settings)
    
    def copy_settings(self, settings : Settings) -> Settings:
        """
        Returns a copy of the given Settings object, with all internal
        attributes copied.

        Args:
            settings (Settings)
        
        Returns:
            (Settings): Copy of the original Settings object.
        """
        return deepcopy(settings)  

    def change_settings(self, settings : Settings, data : Dict[str,str]) \
            -> bool:
        """
        Change the attributes with the provided data of the given settings 
        object. 
        Settings object attributes CANNOT be changed directly. 

        Args:
            settings (Settings): Object whose attributes to change.
            data (Dict[str,str]):
                Mapping from SettingsAttributes string values to their 
                actual values
        
        Returns:
            (bool): True if successful. False otherwise.
        """
        # data keys must be in settings attributes 
        all_attribute_values = \
            [attribute.value for attribute in list(SettingsAttributes)]
        if not all([key in all_attribute_values for key in data.keys()]):
            return False 
        # Otherwise, apply the new settings to the  original settings item. 
        for attr_value, item in data.items():
            for attr in SettingsAttributes:
                if attr.value == attr_value:
                    settings.items[attr] = item 
        return True

    def _contains_keys(self, dictionary : Dict, keys : List[Any]) -> bool:
        """
        Determine if all the keys are contained in the given dictionary. 
        """
        return all([key in dictionary for key in keys])





    

