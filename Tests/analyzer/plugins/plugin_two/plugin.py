# Standard library imports
from typing import Any
# Local imports
from Src.Components.analyzer import Plugin,ApplyConfig,PluginExecutionSummary
# Third party imports

class Plugin(Plugin):

    def __init__(self) -> None:
        pass

    ############################ MODIFIERS ##################################

    def apply_plugin(self, apply_config : ApplyConfig) \
            -> PluginExecutionSummary:
        return PluginExecutionSummary(
            "plugin_two", apply_config.source_paths,{},10,True)
    ############################# GETTERS ###################################