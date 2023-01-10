# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 15:24:33
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-10 15:06:24

from typing import Dict, Any, List
from core.pipeline import Component, ComponentState, ComponentResult
from plugins import PluginManager
from services.organizer import Settings
from ..objects import Payload, AnalysisResults
from plugins import PluginManager

class AnalysisComponent(Component):

    def __init__(
        self,
        plugin_manager : PluginManager
    ):
        self.plugin_manager = plugin_manager

    def __repr__(self):
        raise NotImplementedError()

    def __call__(
        self,
        dependency_outputs : Dict[str, Any]
    ) -> ComponentState:
        """Get a source and the associated settings objects and transcribe"""

        payloads : ComponentResult = dependency_outputs["transcription"]

        for payload in payloads:
            # Get the plugins to apply and apply them.
            settings : Settings = payload.source.settings_profile
            plugins_to_apply = settings.plugins.plugins_to_apply
            suite = settings.plugins.suite
            # TODO: Need to figure out how to pass the base data to the plugins.
            res = self.plugin_manager.apply_suite(
                suite,
                plugins_to_apply,
                payload.transcription_res.utterances
            )
        return ComponentResult(
            state=ComponentState.FAILED,
            result=payload,
            runtime=0
        )





