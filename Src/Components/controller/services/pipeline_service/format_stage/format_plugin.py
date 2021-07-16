# Standard library imports
from abc import abstractmethod
from typing import Dict, Any, List
# Local imports
from .....plugin_manager import Plugin
from .....engines import Utterance
from .format_plugin_input import FormatPluginInput

class FormatPlugin(Plugin):
    """
    Template for plugins to be used in the format stage.
    """

    @abstractmethod
    def apply_plugin(self, dependency_outputs : Dict[str,Any],
             plugin_input : FormatPluginInput) -> Any:
        pass

    @abstractmethod
    def was_successful(self) -> bool:
        pass


