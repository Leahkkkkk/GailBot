# Standard library imports
from abc import abstractmethod
from typing import Dict, Any
# Local imports
from .....plugin_manager import Plugin
from .input import AnalysisPluginInput

class AnalysisPlugin(Plugin):
    """
    Template for plugins to be used in the analysis stage.
    """

    @abstractmethod
    def apply_plugin(self, dependency_outputs : Dict[str,Any],
            plugin_input : AnalysisPluginInput) -> Any:
        """
        Apply this plugin using the given Applyconfig and return the execution
        summary.

        Args:
            dependency_outputs (Dict[str,Any]):
                Mapping from all plugins this plugin is dependant on and their
                outputs.
            apply_config (ApplyConfig)

        Returns:
            (Any)
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


