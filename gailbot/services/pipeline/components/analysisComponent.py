# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 15:24:33
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-09 16:50:05

from typing import Dict, Any, List
from core.pipeline import Component, ComponentState


class AnalysisComponent(Component):

    def __init__(self,*args, **kwargs):
        pass

    def __repr__(self):
        raise NotImplementedError()

    def __call__(
        self,
        dependency_outputs : Dict[str, Any]
    ) -> ComponentState:
        """Get a source and the associated settings objects and transcribe"""
        raise NotImplementedError()
