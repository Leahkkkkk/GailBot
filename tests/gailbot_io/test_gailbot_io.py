# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-08-23 10:16:39
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-08-23 10:24:04

import pytest
from gailbot.core.io import GailBotIO

def test_initialize():
    assert type(GailBotIO()) == GailBotIO