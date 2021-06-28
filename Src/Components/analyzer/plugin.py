# Standard library imports
from typing import Any
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
    def apply_plugin(self, apply_config : ApplyConfig)-> PluginExecutionSummary:
        """
        Apply this plugin using the given Applyconfig and return the execution
        summary.

        Args:
            apply_config (ApplyConfig)

        Returns:
            (PluginExecutionSummary)
        """
        pass
    ############################# GETTERS ###################################

    ############################# SETTERS ###################################

    ########################### PRIVATE METHODS #############################