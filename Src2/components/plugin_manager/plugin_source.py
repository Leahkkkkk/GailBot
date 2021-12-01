# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-11-30 17:59:03
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2021-11-30 18:07:00
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
    plugin_file_path: str
