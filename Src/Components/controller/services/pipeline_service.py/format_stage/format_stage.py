
# Standard library imports
from typing import Any, List, Dict
# Local imports
from .....plugin_manager import PluginManager, PluginManagerSummary, ApplyConfig
from .....organizer import Conversation
from ......utils.threads import ThreadPool
from ......utils.manager import ObjectManager
from ..analysis_stage import AnalysisStageResult
from .result import FormatStageResult


class FormatStage:
    """
    Manages multiple loaded, supported formats.
    """

    def __init__(self) -> None:
        pass

    ############################### MODIFIERS ################################

    def register_format(self, format_name : str,
            data : Dict[str,Dict[str,Any]]) -> None:
        pass

    def format_conversations(self, conversations : Dict[str,Conversation],
            analysis_stage_output : AnalysisStageResult) -> FormatStageResult:
        pass

    ############################### GETTERS ################################

    def is_format(self, format_name : str) -> bool:
        pass

    def get_formats(self) -> List[str]:
        pass

    def is_format_plugin(self, format_name : str, plugin_name : str) -> bool:
        pass

    def get_format_plugins(self, format_name : str) -> List[str]:
        pass





