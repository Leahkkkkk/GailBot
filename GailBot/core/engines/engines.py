# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-02 13:13:08
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-08-23 10:34:47
# Standard library imports
from typing import List, Dict
# Local imports
from .engine import STTEngine
from .watson import WatsonEngine
# Third party imports
from gailbot.core.io import GailBotIO


class Engines:
    """
    Manages different speech to text engines and provides initialized engines
    to users.
    """

    def __init__(self) -> None:
        self.engines = {
            "watson": WatsonEngine
        }
        self.io = GailBotIO()
        # self.network = network

    def get_supported_engines(self) -> List[str]:
        """
        Obtain a list of supported speech to text engines.

        Returns:
            (List[str]): Names of supported engines.
        """
        return list(self.engines.keys())

    def engine(self, engine_type: str) -> STTEngine:
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
