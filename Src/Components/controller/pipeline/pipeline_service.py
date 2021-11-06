
# # Standard imports
from typing import List, Tuple, Dict, Any, Callable

# Local imports
from .logic import GBPipelineLogic
from .transcription_stage import TranscriptionStage
from .plugins_stage import PluginsStage
from .output_stage import OutputStage
from ...utils.manager import ObjectManager
from ...pipeline import Pipeline
from ...plugin_manager import PluginExecutionSummary
from ...services import Source, SettingsProfile
from ...io import IO
from ..configurables.blackboards import PipelineBlackBoard
from .models import Payload, ExternalMethods


class GBPipeline:

    def __init__(self, blackboard: PipelineBlackBoard,
                 external_methods: ExternalMethods) -> None:
        # Vars.
        self.pipeline_name = "transcription_pipeline_service"
        self.pipeline_num_threads = 4
        # Objects
        self.external_methods = external_methods
        self.io = IO()
        self.logic = GBPipelineLogic()
        self.transcription_stage = TranscriptionStage(
            blackboard, external_methods)
        self.plugins_stage = PluginsStage(blackboard, external_methods)
        self.output_stage = OutputStage(blackboard, external_methods)
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
            payloads[name] = self.external_methods.create_payload_from_source(
                source)
        return payloads

    def _parse_plugins_config_file(self, config_path: str) \
            -> Tuple[bool, List[Dict]]:
        try:
            _, data = self.io.read(config_path)
            return (True, data["plugin_configs"])
        except Exception as e:
            print(e)
            return (False, None)
