# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 15:16:01
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-12 14:37:40

from typing import List, Dict, Any
from gailbot.core.pipeline import Pipeline, Component, ComponentResult, ComponentState
from gailbot.plugins import PluginManager
from gailbot.core.utils.logger import makelogger
from ..converter import PayLoadObject
from .components import TranscribeComponent, AnalysisComponent, FormatComponent
logger = makelogger("service pipeline")
class PipelineService:
    def __init__(
        self,
        plugin_manager : PluginManager,
        num_threads: int
    ):

        transcribeComponent = TranscribeComponent()
        analysisComponent = AnalysisComponent(plugin_manager)
        formatComponent = FormatComponent()

        self.pipeline = Pipeline(
            dependency_map={
                "transcription" : [],
                "analysis" : ["transcription"],
                "format" : ["analysis"]
            },
            components ={
                "transcription" : transcribeComponent,
                "analysis"      : analysisComponent,
                "format"        : formatComponent
            },
            num_threads = num_threads # TODO: add to the toml file 
        )

    def __call__(self, payloads : List[PayLoadObject]):
        res = self.pipeline(
            base_input= payloads
        )
        for name, result in res.items():
            if not result == ComponentState.SUCCESS:
                return False 
        return True

        
