# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-11-05 21:08:01
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2021-12-02 16:22:39

# # Standard imports
from typing import List, Tuple, Dict, Any, Callable
from ..io import IO
from ..shared_models import Source, SourceHook, Settings, SettingsHook,\
    SettingsProfile
from ..pipeline import Pipeline
from .logic import GBPipelineLogic
from .transcription_stage import TranscriptionStage
from .plugins_stage import PluginsStage
from .output_stage import OutputStage
from .payload import Payload

# Local imports


class PipelineService:

    def __init__(self) -> None:
        # Vars.
        self.pipeline_name = "transcription_pipeline_service"
        self.pipeline_num_threads = 4
        self.io = IO()
        self.logic = GBPipelineLogic()
        self.pipeline = Pipeline(self.pipeline_name, self.pipeline_num_threads)
        self.pipeline.set_logic(self.logic)
        self.transcription_stage = TranscriptionStage()
        self.plugins_stage = PluginsStage()
        self.output_stage = OutputStage()
        self.pipeline.add_component(
            "transcription_stage", self.transcription_stage)
        self.pipeline.add_component(
            "plugins_stage", self.plugins_stage, ["transcription_stage"])
        self.pipeline.add_component(
            "output_stage", self.output_stage, ["plugins_stage"])

    def register_plugins(self, config_path: str) -> List[str]:
        success, configs = self._parse_plugins_config_file(config_path)
        return self.plugins_stage.register_plugins(configs) if success else []

    def execute(self, sources: List[Source]) -> Any:
        payloads = dict()
        for source in sources:
            payloads[source.identifier] = Payload(source)
        self.pipeline.set_base_input(payloads)
        self.pipeline.execute()

    def _parse_plugins_config_file(self, config_path: str) \
            -> Tuple[bool, List[Dict]]:
        try:
            _, data = self.io.read(config_path)
            return (True, data["plugin_configs"])
        except Exception as e:
            print(e)
            return (False, None)
