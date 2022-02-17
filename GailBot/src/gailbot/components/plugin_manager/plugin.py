# Standard library imports
from typing import Any, Dict
from abc import ABC, abstractmethod
# Local imports
from .apply_config import ApplyConfig
from .plugin_execution_summary import PluginExecutionSummary

class Plugin(ABC):
    """
    Template superclass for any plugin that may be used with the Analyzer
    component.
    """

    def __init__(self) -> None:
        pass

    ############################ MODIFIERS ##################################

    @abstractmethod
    def apply_plugin(self, dependency_outputs : Dict[str,Any],
             *args, **kwargs) -> Any:
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
    ############################# GETTERS ###################################

    @abstractmethod
    def was_successful(self) -> bool:
        """
        Determine if the plugin executed successfully.

        Returns:
            (bool): True if the plugin was successful. False otherwise.
        """
        pass

    ############################# SETTERS ###################################

    ########################### PRIVATE METHODS #############################