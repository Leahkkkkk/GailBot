# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 15:16:01
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-08 15:35:16

from typing import List, Dict, Any
from core.pipeline import Pipeline, Component
from services.baseObjects import Payload
from .components import TranscribeComponent, AnalysisComponent, FormatComponent

class PipelineService:

    def __init__(self):

        transcribeComponent = TranscribeComponent()
        analysisComponent = analysisComponent()
        formatComponent = formatComponent()

        self.pipeline = Pipeline(
            dependency_map={
                "transcription" : None,
                "analysis" : ["transcription"],
                "format" : ["analysis"]
            },
            components =[
                transcribeComponent,
                analysisComponent,
                formatComponent
            ]

        )

    def __call__(self, payloads : List[Payload]):
        # Passing in one at a time - but this needs to be multithreaded.
        # Each component should be multithreading internally if possible.
        self.pipeline(payloads)

