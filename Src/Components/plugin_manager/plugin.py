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
            apply_config (ApplyConfig)

        Returns:
            (Any)
        """
        pass
    ############################# GETTERS ###################################

    @abstractmethod
    def was_successful(self) -> bool:
        pass

    ############################# SETTERS ###################################

    ########################### PRIVATE METHODS #############################