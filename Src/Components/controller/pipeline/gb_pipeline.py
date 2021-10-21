
# # Standard imports
from typing import List, Tuple, Dict, Any
# Local imports
from .logic import GBPipelineLogic
from .stages import TranscriptionStage, PluginsStage, OutputStage
from ...utils.manager import ObjectManager
from ...pipeline import Pipeline
from ...plugin_manager import PluginExecutionSummary
from ...services import Source, SettingsProfile


class GBPipeline:

    def __init__(self) -> None:
        # Vars.
        self.pipeline_name = "transcription_pipeline_service"
        self.pipeline_num_threads = 4
        # Objects
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
        pass

    def execute(self, sources: Dict[str, Source]) -> Any:
        pass

    def get_plugin_names(self) -> List[str]:
        pass
