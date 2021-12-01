# Standard library imports
from typing import Callable, Any, List, Dict
# Local imports
from .stream import Stream
# Third party imports
from abc import ABC

class Logic(ABC):
    """
    Abstract class that should be subclassed.
    Responsible for defining the execution logic for a Pipeline object.
    """

    def __init__(self) -> None:
        self.callables = dict()

    def get_preprocessor(self, component_name : str) \
            -> Callable[[Dict[str,Stream]], Any]:
        """
        Obtain the pre_processor associated with the specified component.
        The preprocessor expects a dictionary of Stream objects and should
        format the data as expected by the processor for the same component.

        Args:
            component_name (str): Name of the component

        Returns:
            (Callable[[Dict[str,Stream]], Any]):
                Callable that takes in a mapping from name to Stream object
                and outputs an object that is expected by the processor for
                the same component.
        """
        try:
            return self.callables[component_name]["pre_processor"]
        except:
            pass

    def get_processor(self, component_name : str) \
            -> Callable[[object, Any], Any]:
        """
        Obtain the processor for the specified component.
        The processor expects as input the output of the preprocessor for the
        same component and should output an object that is accepted by the
        corresponding post-processor.

        Args:
            component_name (str): Name of the component

        Returns:
            (Callable[[object, Any], Any]):
                Callable that takes as input the output of the corresponding
                pre-processor and produces and output that is accepted by the
                corresponding post-processor.
        """
        try:
            return self.callables[component_name]["processor"]
        except:
            pass

    def get_postprocessor(self, component_name : str) -> Callable[[Any],Stream]:
        """
        Obtain the post-processor for the specified component.
        The post-processor expects as input the output of the processor and
        outputs a Stream object.

        Args:
            component_name (str): Name of the component

        Returns:
            (Callable[[Any],Stream]):
                Callable that takes as input the output of the processor and
                outputs a Stream object.
        """
        try:
            return self.callables[component_name]["post_processor"]
        except:
            pass

    def is_component_supported(self, component_name : str) -> bool:
        """
        Determine if the specified component is supported by the Logic

        Args:
            component_name (str): Name of the component

        Returns:
            (bool): True if the component is supported. False otherwise.
        """
        return component_name in self.callables.keys()

    def get_supported_component_names(self) -> List[str]:
        """
        Obtain all components that are supported by the Logic.

        Returns:
            (List[str]): List of all support component names.
        """
        return list(self.callables.keys())

    def _add_component_logic(self, component_name : str,
            pre_processor :Callable[[Dict[str,Stream]], Any],
            processor : Callable[[object, Any], Any],
            post_processor : Callable[[Any],Stream]) -> None:
        """
        Add the given component to the post-processor.
        Should be used by the subclasses to add a component to Logic.
        """
        self.callables[component_name] = {
            "pre_processor" : pre_processor,
            "processor" : processor,
            "post_processor" : post_processor}

