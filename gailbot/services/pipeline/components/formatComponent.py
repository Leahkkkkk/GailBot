# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 15:25:29
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-10 15:18:02


from typing import Dict, Any, List
from core.pipeline import Component, ComponentState, ComponentResult
from plugins import PluginManager
from services.organizer import Settings
from plugins import PluginManager
from ..objects import Payload, AnalysisResults, PayloadOutputWriter

class FormatComponent(Component):

    def __init__(self):
        pass

    def __repr__(self):
        raise NotImplementedError()

    def __call__(
        self,
        dependency_outputs : Dict[str, Any]
    ) -> ComponentState:

        """Get a source and the associated settings objects and transcribe"""
        payloads : ComponentResult = dependency_outputs["analysis"]

        for payload in payloads:
            PayloadOutputWriter.write_output(payload)

        return ComponentResult(
            state=ComponentState.FAILED,
            result=None,
            runtime=0
        )



