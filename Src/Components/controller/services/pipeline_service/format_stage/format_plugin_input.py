# Standard imports
from Src.Components.plugin_manager.plugin_execution_summary import PluginExecutionSummary
from typing import Dict,  Any, List
from dataclasses import dataclass
# Local imports
from .....engines import Utterance
from ..pipeline_plugin_input import PipelinePluginInput
from ..pipeline_payload import SourcePayload


class FormatPluginInput(PipelinePluginInput):

    def __init__(self, payload : SourcePayload) -> None:
        super().__init__(payload)

    ################################# GETTERS ###############################

    def get_analysis_plugin_outputs(self) -> Dict[str,Any]:
        if not self.payload.is_analyzed():
            return {}
        # Generate the output from the plugin summary
        plugin_outputs = dict()
        plugin_summaries = self.payload.get_analysis_plugin_summaries()
        for name, summary in plugin_summaries.items():
            summary : PluginExecutionSummary
            plugin_outputs[name] = summary.output
        return plugin_outputs






