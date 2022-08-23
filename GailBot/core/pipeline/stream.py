# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-08-23 10:02:56
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-08-23 10:58:51
# Standard library imports
from typing import Any
# Local imports
from gailbot.utils.models import IDictModel
# Third party imports


class Stream(IDictModel):
    """
    Object that stores information and is passed between components in a
    Pipeline.

    Inherits:
        (IDictModel)
    """

    def __init__(self, data: Any = None) -> None:
        """
        Args:
            data (Any): Data to store.
        """
        super().__init__()
        self.items = {
            "data": data}

    def get_stream_data(self) -> Any:
        """
        Obtain the data stored in the stream

        Returns:
            (Any): Data in the stream
        """
        return self.get("data")[1]

    def set_stream_data(self, data: Any) -> bool:
        """
        Set the data stored in the stream.

        Args:
            data (Any)

        Returns:
            (bool): True if successfully stored. False otherwise.
        """
        return self.set("data", data)
