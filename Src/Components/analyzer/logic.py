# Standard library imports
from typing import Callable, Dict, Any
# Local imports
from ..pipeline import Logic, Stream
from .plugin import Plugin
from .models.plugin_execution_summary import PluginExecutionSummary

class PluginPipelineLogic(Logic):

    def __init__(self) -> None:
        super().__init__()
        # Adding all logic methods

    def get_preprocessor(self, component_name : str) \
            -> Callable[[Dict[str,Stream]], Any]:
        return self._preprocessor_plugin

    def get_processor(self, component_name : str) \
            -> Callable[[object, Any], Any]:
        return self._processor_plugin

    def get_postprocessor(self, component_name : str) -> Callable[[Any],Stream]:
        return self._post_processor_plugin

    def is_component_supported(self, component_name : str) -> bool:
        return True

    ########################### PRIVATE METHODS #############################

    def _preprocessor_plugin(self, streams : Dict[str,Stream]) -> Dict:
        return streams["base"].get_stream_data()

    def _processor_plugin(self, instantiated_obj : object, preprocessed_data : Dict) \
            -> PluginExecutionSummary:
        plugin : Plugin = instantiated_obj["plugin"]
        # TODO: Need to get input to this method somehow.
        return plugin.apply_plugin("","")

    def _post_processor_plugin(self, summary : PluginExecutionSummary) -> Stream:
        return Stream(summary)