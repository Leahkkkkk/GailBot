# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-08-23 11:06:19
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-08-23 11:07:20


import pytest
from gailbot.plugin.plugin_manager import PluginManager

def test_initialize():
    assert type(PluginManager()) == PluginManager