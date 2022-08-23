# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-08-23 10:59:48
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-08-23 11:00:45

import pytest
from gailbot.core.pipeline import Pipeline

def test_initialize():
    assert type(Pipeline("test")) == Pipeline