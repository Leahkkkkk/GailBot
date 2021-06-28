# Standard library imports
from typing import Any, List, Dict
# Local imports
from Src.Components.analyzer import Plugin
# Third party imports

class Plugin(Plugin):

    def __init__(self) -> None:
        pass

    ############################ MODIFIERS ##################################

    def apply_plugin(self, paths : List[str]) \
            -> Dict[str,str]:
        result = dict()
        for path in paths:
            result[path] = path
        return result
    ############################# GETTERS ###################################

    def was_successful(self) -> bool:
        return True