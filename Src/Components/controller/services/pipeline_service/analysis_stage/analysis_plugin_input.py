# Standard imports
from dataclasses import dataclass
from typing import Dict, List
# Local imports
from .....engines import Utterance
from ..pipeline_plugin_input import PipelinePluginInput
from ..pipeline_payload import SourcePayload

import sys
class AnalysisPluginInput(PipelinePluginInput):

    def __init__(self, payload : SourcePayload) -> None:
        super().__init__(payload)

    ################################# GETTERS ###############################

    def get_source_to_audio_map(self) -> Dict[str,str]:
        return self.payload.get_source_to_audio_map()
