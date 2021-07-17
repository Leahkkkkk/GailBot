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
        """
        Obtain a mapping from source file name to its audio file used
        for transcription.

        Returns:
            (Dict[str,str]):
                Map from source file name to associated audio file path.
        """
        return self.payload.get_source_to_audio_map()
