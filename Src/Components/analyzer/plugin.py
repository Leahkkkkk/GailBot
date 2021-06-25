# Standard library imports
from typing import Any
from abc import ABC, abstractmethod
# Local imports
from .apply_config import ApplyConfig
from .plugin_execution_summary import PluginExecutionSummary



class Plugin(ABC):

    def __init__(self) -> None:
        pass

    ############################ MODIFIERS ##################################

    @abstractmethod
    def apply_plugin(self, apply_config : ApplyConfig)-> PluginExecutionSummary:
        pass
    ############################# GETTERS ###################################

    ############################# SETTERS ###################################

    ########################### PRIVATE METHODS #############################