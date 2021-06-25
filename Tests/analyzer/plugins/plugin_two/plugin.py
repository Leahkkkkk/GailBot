# Standard library imports
from typing import Any
# Local imports
from Src.Components.analyzer import Plugin, ApplyConfig, Plugin, PluginExecutionSummary
# Third party imports

class Plugin(Plugin):

    def __init__(self) -> None:
        pass

    ############################ MODIFIERS ##################################

    def apply_plugin(self, apply_config : ApplyConfig) \
            -> PluginExecutionSummary:
        print("Applying plugin two")
    ############################# GETTERS ###################################

