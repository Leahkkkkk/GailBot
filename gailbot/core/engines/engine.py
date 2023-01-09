# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-06 15:49:53
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-09 11:21:54


from typing import Any, Dict

class Engine:

    def __init__(self, *args, **kwargs):
        pass

    def __repr__(self):
        """Returns all the configurations and additional metadata"""
        raise NotImplementedError()

    # def configure(self, *args, **kwargs) -> bool:
    #     """Configure all attributes"""
    #     pass

    # def get_configurations(self, *args, **kwargs) -> Dict:
    #     """Get dictionary of all configured attrs."""
    #     pass

    def transcribe(self, *args, **kwargs) -> Any:
        """Use the engine to transcribe an item"""
        pass









