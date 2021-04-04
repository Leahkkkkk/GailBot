# Standard library imports
from typing import Callable, Any, List, Dict
# Local imports
from .stream import Stream

# Third party imports

class Logic:

    def __init__(self) -> None:
        self.callables = dict()

    def get_preprocessor(self, component_name : str) \
            -> Callable[[Dict[str,Stream]], Any]:
        try:
            return self.callables[component_name]["pre_processor"]
        except:
            pass

    def get_processor(self, component_name : str) \
            -> Callable[[object, Any], Any]:
        try:
            return self.callables[component_name]["processor"]
        except:
            pass

    def get_postprocessor(self, component_name : str) -> Callable[[Any],Stream]:
        try:
            return self.callables[component_name]["post_processor"]
        except:
            pass

    def is_component_supported(self, component_name : str) -> bool:
        return component_name in self.callables.keys()

    def get_supported_component_names(self) -> List[str]:
        return list(self.callables.keys())


    def _add_component_logic(self, component_name : str,
            pre_processor :Callable[[Dict[str,Stream]], Any],
            processor : Callable[[object, Any], Any],
            post_processor : Callable[[Any],Stream]) -> None:
        self.callables[component_name] = {
            "pre_processor" : pre_processor,
            "processor" : processor,
            "post_processor" : post_processor}

