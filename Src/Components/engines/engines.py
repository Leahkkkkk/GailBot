# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-02 13:13:08
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2021-12-02 15:00:50
# Standard library imports
from typing import List, Dict
# Local imports
from .engine import Engine
from .watson import WatsonEngine
from ..io import IO
# Third party imports


class Engines:
    """
    Manages different speech to text engines and provides initialized engines
    to users.
    """

    def __init__(self, io: IO) -> None:
        self.engines = {
            "watson": WatsonEngine
        }
        self.io = io
        # self.network = network

    def get_supported_engines(self) -> List[str]:
        """
        Obtain a list of supported speech to text engines.

        Returns:
            (List[str]): Names of supported engines.
        """
        return list(self.engines.keys())

    def engine(self, engine_type: str) -> Engine:
        """
        Obtain an initialized engine of the specified type.
        Raises ExceptionUnexpected if the engine_type is not supported.

        Args:
            engine_type (str): Type of the engine. Must be a supported engine.

        Returns:
            (Engine)
        """
        if not engine_type in self.engines.keys():
            raise Exception()
        return self.engines[engine_type](self.io)
