# Standard library imports
from abc import abstractmethod
from typing import Dict, Any
# Local imports
from .....plugin_manager import Plugin
from .input import FormatPluginInput
class FormatPlugin(Plugin):

    @abstractmethod
    def apply_plugin(self, dependency_outputs : Dict[str,Any],
            plugin_input : FormatPluginInput) -> Any:
        pass

    @abstractmethod
    def was_successful(self) -> bool:
        pass


