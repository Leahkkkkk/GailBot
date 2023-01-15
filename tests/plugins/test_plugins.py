# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-15 13:37:25
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-15 14:58:13

import sys
import os

from gailbot.plugins import (
    PluginManager,
    PluginSuite,
    Plugin,
    Methods
)

from typing import Dict, List, Any


PLUGIN_MANAGER_WS = "./plugins_ws"

class GBPluginMethods(Methods):

    def __init__(self):
        pass

    @property
    def audios(self) -> Dict[str,str]:
        raise NotImplementedError()

    @property
    def utterances(self) -> Dict[str,Dict]:
        raise NotImplementedError()

    @property
    def save_dir(self) -> str:
        raise NotImplementedError()


def test_manager():
    pass