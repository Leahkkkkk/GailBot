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
        """
        This method is called to apply the plugin on a single source.

        Args:
            dependency_outputs (Dict[str,Any]):
                Map from any plugins this one is dependant on to their outputs.
            plugin_input (FormatPluginInput):
                Object that provides utility methods for this source.

        Returns:
            (Any): This is stored as the output for this plugin.
        """
        pass

    @abstractmethod
    def was_successful(self) -> bool:
        """
        Determine if the plugin is successful.

        Returns:
            (bool): True if the plugin is successful, False otherwise.
        """
        pass


