# Standard library imports
# Local imports
from Src.Components.controller.services.pipeline_service import \
    AnalysisPlugin,AnalysisPluginInput
from Src.Components.engines import Utterance, UtteranceAttributes

class Plugin(AnalysisPlugin):


    def apply_plugin(self, plugin_input : AnalysisPluginInput) -> None:
        print("in TCU plugin")

    def was_successful(self) -> bool:
        return True