# Standard imports
from typing import Dict, Any, List
import re
# Local imports
from Src.Components.controller.services import AnalysisPluginInput, \
    AnalysisPlugin, Utt
from Src.default_plugins.analysis_plugins.turn import Turn


class FTOAnalysis(AnalysisPlugin):

    def __init__(self) -> None:
        pass

    def apply_plugin(self, dependency_outputs : Dict[str,Any],
             plugin_input : AnalysisPluginInput) -> Any:
        pass

    def was_successful(self) -> bool:
        pass
