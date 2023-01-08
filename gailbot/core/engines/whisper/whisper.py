# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 12:43:29
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-08 12:50:11

from typing import Dict, Any

from ..engine import Engine


class Whisper(Engine):

    def __init__(self):
        pass

    def __str__(self):
        """Returns the name of the function"""
        raise NotImplementedError()

    def __repr__(self):
        """Returns all the configurations and additional metadata"""
        raise NotImplementedError()

    def configure(self, *args, **kwargs) -> bool:
        """Configure all attributes"""
        pass

    def get_configurations(self, *args, **kwargs) -> Dict:
        """Get dictionary of all configured attrs."""
        pass

    def transcribe(self, *args, **kwargs) -> Any:
        """Use the engine to transcribe an item"""
        pass