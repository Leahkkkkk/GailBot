# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 13:22:45
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-12 13:29:53

from typing import Any, Dict
from abc import ABC, abstractmethod
# Local imports


class Methods:
    """
    Methods that will be passed to a plugin.
    These can be custom defined and may be useful as 
    a wrapper around objects
    that may want to be passed to a plugin.
    """

    def __init__(self):
        pass

class Plugin:
    """
    Template superclass for any plugin.
    """

    def __init__(self) -> None:
        self.successful = False
        pass

    @property
    def is_successful(self) -> bool:
        return self.successful

    def apply(
        self,
        dependency_outputs : Dict[str, Any],
        methods : Methods,
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

