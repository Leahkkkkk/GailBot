# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-08-23 10:41:52
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-08-23 10:42:33

import pytest

from gailbot.core.network import Network

def test_initialize():
    assert type(Network()) == Network