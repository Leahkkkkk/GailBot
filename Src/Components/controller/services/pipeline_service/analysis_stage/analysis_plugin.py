# Standard library imports
from abc import abstractmethod
from typing import Dict, Any
# Local imports
from .....plugin_manager import Plugin
from .analysis_plugin_input import AnalysisPluginInput

class AnalysisPlugin(Plugin):
    """
    Template for plugins to be used in the analysis stage.
    """

    @abstractmethod
    def apply_plugin(self, dependency_outputs : Dict[str,Any],
            plugin_input : AnalysisPluginInput) -> Any:
        """
        This method is called to apply the plugin on a single source.

        Args:
            dependency_outputs (Dict[str,Any]):
                Map from any plugins this one is dependant on to their outputs.
            plugin_input (AnalysisPluginInput):
                Object that provides utility methods for this source.

        Returns:
            (Any): This is stored as the output for this plugin.
        """
        pass

    @abstractmethod
    def was_successful(self) -> bool:
        """
        Determine if the plugin executed successfully.

        Returns:
            (bool): True if the plugin was successful. False otherwise.
        """
        pass


