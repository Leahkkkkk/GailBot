# Standard library imports

# Local imports
from Src.Components.analyzer import Plugin, PluginDetails, PluginSummary
# Third party imports

class Plugin(Plugin):

    def __init__(self) -> None:
        pass

    ############################ MODIFIERS ##################################

    def apply_plugin(self, source_path : str, workspace_path : str) \
            -> PluginSummary:
        print("Applying plugin one")
    ############################# GETTERS ###################################

    def get_details(self) -> PluginDetails:
        pass
