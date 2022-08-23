# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-08-23 11:56:06
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-08-23 11:56:33


import pytest
from gailbot.controller import GailBotController

def test_initialize():
    controller = GailBotController("./")