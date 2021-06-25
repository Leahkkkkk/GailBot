# Standard library imports
from typing import Any
# Local imports
from Src.Components.analyzer import Plugin
# Third party imports

class Plugin(Plugin):

    def __init__(self) -> None:
        pass

    ############################ MODIFIERS ##################################

    def apply_plugin(self, source_path : str, workspace_path : str) \
            -> Any:
        print("Applying plugin two")
    ############################# GETTERS ###################################

