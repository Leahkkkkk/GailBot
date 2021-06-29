# Standard library imports
from abc import abstractmethod
from typing import Dict, Any
# Local imports
from ....plugin_manager import Plugin
from .analysis_plugin_input import AnalysisPluginInput

class AnalysisPlugin(Plugin):

    @abstractmethod
    def apply_plugin(self, input : AnalysisPluginInput) -> Any:
        pass

    @abstractmethod
    def was_successful(self) -> bool:
        pass


