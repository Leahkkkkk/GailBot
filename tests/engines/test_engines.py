# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-08-23 10:33:32
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-08-23 10:37:08


import pytest
from gailbot.core.engines import Engines

def test_initialize():
    assert type(Engines()) == Engines
    engines = Engines()
    print(engines.engine("watson"))

