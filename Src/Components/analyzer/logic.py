# Standard library imports
from typing import Callable, Dict, Any
# Local imports
from ..pipeline import Logic, Stream
from .plugin import Plugin
from .plugin_source import PluginSource
from .apply_config import ApplyConfig

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

    def _processor_plugin(self, plugin_source :  PluginSource,
            apply_configs : Dict[str,ApplyConfig]) \
            -> Any:
        apply_config = apply_configs[plugin_source.plugin_name]
        plugin : Plugin = plugin_source.plugin_object
        return plugin.apply_plugin(apply_config)

    def _post_processor_plugin(self, summary : Any) -> Stream:
        return Stream(summary)