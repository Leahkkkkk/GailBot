from typing import Dict, Any, List
from abc import abstractmethod
from ....plugin_manager import Plugin


class PluginMethodSuite:
    pass


class GBPlugin(Plugin):
    @abstractmethod
    def apply_plugin(self, dependency_outputs: Dict[str, Any],
                     plugin_method_suite: PluginMethodSuite) -> Any:
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


class PluginsStage:

    def __init__(self) -> None:
        pass

    def apply_plugins(self) -> None:
        pass
