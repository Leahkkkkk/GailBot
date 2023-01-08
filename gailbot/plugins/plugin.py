# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 13:22:45
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-08 13:40:32

from typing import Any, Dict
from abc import ABC, abstractmethod
# Local imports


class Plugin:
    """
    Template superclass for any plugin.
    """

    def __init__(self) -> None:
        pass


    def apply(
        self,
        dependency_outputs : Dict[str, Any],
        *args,
        **kwargs
    ) -> Any:
        """
        Wrapper for plugin algorithm that has access to dependencies =,
        Args:
            dependency_outputs (Dict[str,Any]):
                Mapping from all plugins this plugin is dependant on and their
                outputs.
        """
        raise NotImplementedError()

    def is_successful(self) -> bool:
        return False
