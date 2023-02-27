# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-11-30 18:16:52
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2021-11-30 18:16:53
# Standard library imports
from typing import Tuple, Any
# Third party imports
from abc import ABC


class IDictModel(ABC):
    """
    Abstract model class that stores information internally as a dictionary and
    can be inherited by sub-class that define the items that are used by this
    class.
    """

    def __init__(self) -> None:
        super().__init__()
        self.items = dict()

    def get(self, attr: str) -> Tuple[bool, Any]:
        """
        Returns the value associated with the attribute if that attribute exists
        in the models attributes.

        Args:
            attr (Any)

        Returns:
            (Tuple[bool,Any]): True + data is attribute exists.
                            False + None if the attribute is invalid.
        """
        try:
            return (True, self.items[attr])
        except:
            return (False, None)

    def set(self, attr: str, data: Any) -> bool:
        """
        Sets the given attribute to the data if it exists in the models attributes.

        Args:
            attr (Any)
            data (Any): Data associated with the attribute.

        Returns:
            (bool): true if successful. False otherwise.
        """
        if attr in self.items.keys():
            self.items[attr] = data
            return True
        return False

    def count(self) -> int:
        """
        Return the number of items stored in this model.

        Returns:
            (int): No. of items stored in the model.
        """
        return len(self.items.keys())
