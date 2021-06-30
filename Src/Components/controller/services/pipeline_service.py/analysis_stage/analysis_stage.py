# Standard library imports
from typing import Any, List, Dict
# Local imports
from .....plugin_manager import PluginManager, PluginManagerSummary, ApplyConfig
from .....organizer import Conversation
from ......utils.threads import ThreadPool
from ..transcription_stage import TranscriptionStageResult
from .result import AnalysisStageResult

# TODO: Methods to select / deselect plugins.
class AnalysisStage:

    def __init__(self) -> None:
        ## Objects
        self.plugin_manager = PluginManager()
        self.thread_pool = ThreadPool(4) # TODO: Remove hard-code.
        self.thread_pool.spawn_threads()

    ########################## MODIFIERS ######################################

    def register_plugin_from_data(self, data : Dict[str,Any]) -> bool:
        return self.plugin_manager.register_plugin_using_config_data(data)

    def analyze(self, conversations : Dict[str,Conversation],
            transcription_stage_output : TranscriptionStageResult) \
                -> AnalysisStageResult:
        pass

    ########################## GETTERS #########################################

    def is_plugin(self, plugin_name : str) -> bool:
        return self.plugin_manager.is_plugin(plugin_name)

    def get_plugin_names(self) -> List[str]:
        return self.plugin_manager.get_plugin_names()