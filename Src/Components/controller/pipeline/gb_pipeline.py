
# # Standard imports
from typing import List, Tuple, Dict, Any

from Src.components.controller.pipeline.models import Payload
# Local imports
from .logic import GBPipelineLogic
from .stages import TranscriptionStage, PluginsStage, OutputStage
from ...utils.manager import ObjectManager
from ...pipeline import Pipeline
from ...plugin_manager import PluginExecutionSummary
from ...services import Source, SettingsProfile
from ...io import IO


class GBPipeline:

    def __init__(self) -> None:
        # Vars.
        self.pipeline_name = "transcription_pipeline_service"
        self.pipeline_num_threads = 4
        # Objects
        self.io = IO()
        self.logic = GBPipelineLogic()
        self.transcription_stage = TranscriptionStage()
        self.plugins_stage = PluginsStage()
        self.output_stage = OutputStage()
        # Initialize pipeline
        self.pipeline = Pipeline(self.pipeline_name, self.pipeline_num_threads)
        self.pipeline.set_logic(self.logic)
        self.pipeline.add_component(
            "transcription_stage", self.transcription_stage)
        self.pipeline.add_component(
            "plugins_stage", self.plugins_stage, ["transcription_stage"])
        self.pipeline.add_component(
            "output_stage", self.output_stage, ["plugins_stage"])

    def register_plugins(self, config_path: str) -> List[str]:
        success, configs = self._parse_plugins_config_file(config_path)
        return self.plugins_stage.register_plugins(configs) if success else []

    def execute(self, sources: Dict[str, Source]) -> Any:
        self.pipeline.set_base_input(
            self._generate_payloads_from_sources(sources))
        self.pipeline.execute()

    def get_plugin_names(self) -> List[str]:
        pass

    def _generate_payloads_from_sources(self, sources: Dict[str, Source]) \
            -> Dict[str, Payload]:
        payloads = dict()
        for name, source in sources.items():
            payloads[name] = Payload(source)
        return payloads

    def _parse_plugins_config_file(self, config_path: str) \
            -> Tuple[bool, List[Dict]]:
        try:
            _, data = self.io.read(config_path)
            return (True, data["plugin_configs"])
        except Exception as e:
            print(e)
            return (False, None)
