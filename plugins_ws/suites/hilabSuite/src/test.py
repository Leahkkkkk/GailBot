# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-16 12:04:54
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-16 12:07:59


from gailbot import Plugin, GBPluginMethods
from typing import Dict, Any

class TestPlugin1:

    def __init__(self) -> None:
        self._successful = False

    @property
    def is_successful(self) -> bool:
        return self._successful

    def apply(
        self,
        dependency_outputs : Dict[str, Any],
        methods : GBPluginMethods,
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
        print(
            f"Applying plugin suite: {self}\n"
            f"dependency_outputs: {dependency_outputs}\n"
            f"methods: {methods}"
        )
        self._successful = True


