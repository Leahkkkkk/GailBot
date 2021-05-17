# Standard library imports
from typing import Any, List
# Local imports
from ...utils.models import IDictModel
# Third party imports

class Settings(IDictModel):

    def __init__(self, attrs : List[str]) -> None:
        super().__init__()
        for attr in attrs:
            self._add_attribute(attr)

    def is_configured(self) -> bool:
        """
        Determine if the Paths object has successfully read data.

        Returns:
            (bool): True if data has been successfully read. False otherwise.
        """
        return all([v != None for v in self.items.values()])

    def _has_attribute(self, attr : str) -> bool:
        """
        Determine if the settings object has the given attribute.
        """
        return attr in self.items

    def _add_attribute(self, attr : str) -> None:
        """
        Add the attribute to the list of accepted attributes.

        Args:
            attr (str): Attribute name
        """
        self.items[attr] = None

    def _set_value(self, attr : str, data : Any) -> bool:
        """
        Set the value for the given attribute if it is accepted.

        Args:
            attr (str): Attribute to change
            data (Any): Data to be set as the value for that attribute

        Returns:
            (bool): True if set. False if not set or if attr is not accepted.

        """
        return self.set(attr,data)
