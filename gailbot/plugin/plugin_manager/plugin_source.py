# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-02 13:13:08
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2021-12-07 12:55:36
# Standard library imports
from typing import List, Any
from dataclasses import dataclass
from .plugin import Plugin


@dataclass
class PluginSource:
    """
    Internal representation of a plugin in the manager.
    """
    plugin_name: str
    plugin_object: Plugin
    plugin_dependencies: List[str]
    number_of_dependencies: int
    plugin_file_path: str
