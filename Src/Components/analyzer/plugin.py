# Standard library imports
from abc import ABC, abstractmethod
# Local imports
from .models.plugin_execution_summary import PluginExecutionSummary
from .models.apply_config import ApplyConfig


class Plugin(ABC):

    def __init__(self) -> None:
        pass

    ############################ MODIFIERS ##################################

    @abstractmethod
    def apply_plugin(self, apply_config : ApplyConfig) \
            -> PluginExecutionSummary:
        pass
    ############################# GETTERS ###################################

    ############################# SETTERS ###################################

    ########################### PRIVATE METHODS #############################