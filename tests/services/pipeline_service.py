# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-08-23 11:39:42
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-08-23 11:52:49
import pytest
from gailbot.services.pipeline_service import PipelineService

def test_initialize():
    assert type(PipelineService()) == PipelineService