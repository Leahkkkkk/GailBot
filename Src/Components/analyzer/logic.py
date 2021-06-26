# Standard library imports
from Src.Components.analyzer.plugin_execution_summary import PluginExecutionSummary
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
        """
        Override the super class method to make sure same method is returned
        for any component.
        """
        return self._preprocessor_plugin

    def get_processor(self, component_name : str) \
            -> Callable[[object, Any], Any]:
        """
        Override the super class method to make sure same method is returned
        for any component.
        """
        return self._processor_plugin

    def get_postprocessor(self, component_name : str) -> Callable[[Any],Stream]:
        """
        Override the super class method to make sure same method is returned
        for any component.
        """
        return self._post_processor_plugin

    def is_component_supported(self, component_name : str) -> bool:
        """
        In this pipeline, any component may be supported.
        """
        return True

    ########################### PRIVATE METHODS #############################

    def _preprocessor_plugin(self, streams : Dict[str,Stream]) \
            -> Dict[str,ApplyConfig]:
        """
        Extract apply configs from the base input.
        """
        return streams["base"].get_stream_data()

    def _processor_plugin(self, plugin_source :  PluginSource,
            apply_configs : Dict[str,ApplyConfig]) \
            -> PluginExecutionSummary:
        """
        Applies the plugin specified by the plugin source using the given
        ApplyConfig.
        Returns PluginExecutionSummary for the specified plugin.
        """
        apply_config = apply_configs[plugin_source.plugin_name]
        plugin : Plugin = plugin_source.plugin_object
        return plugin.apply_plugin(apply_config)

    def _post_processor_plugin(self, summary : PluginExecutionSummary) -> Stream:
        """
        Package the PluginExecutionSummary as a Stream.
        """
        return Stream(summary)