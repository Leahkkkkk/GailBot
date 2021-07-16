# Standard imports
from typing import Any, Dict, List
from copy import deepcopy
# Local imports
from ....engines import Utterance
from .plugin_utterance_wrapper import Utt
from .pipeline_payload import SourcePayload

class PipelinePluginInput:

    def __init__(self, payload : SourcePayload) -> None:
        self.payload = payload
    ################################# MODIFIERS ###############################

    def add_to_source(self, identifier : str, path : str,
            copy : bool = False) -> bool:
        return self.payload.add_to_source(
            identifier,path,"permanent",copy)

    def write_to_file(self, identifier : str, file_name : str,
            extension : str, data : Any, overwrite : bool = False) -> bool:
        return self.payload.write_to_file(
            identifier, "permanent",file_name, extension, data, overwrite)

    ################################# GETTERS ###############################

    def get_source_name(self) -> str:
        return self.payload.get_source_name()

    def get_workspace_path(self) -> str:
        return self.payload.get_workspace_path()

    def result_directory_path(self) -> str:
        return self.payload.get_result_directory_path()

    def get_utterances(self) -> Dict[str,List[Utterance]]:
        utterances_wrap_map = dict()
        utterance_map =  self.payload.get_conversation().get_utterances()
        for name, utterances in utterance_map.items():
            utterances_wrap_map[name] = self._wrap_utterances(
                utterances)
        return utterances_wrap_map

    def get_source_paths(self) -> Dict[str,str]:
        return self.payload.get_conversation().get_source_file_paths()

    ############################# PRIVATE METHODS ###########################

    def _wrap_utterances(self, utterances : List[Utterance]) -> List[Utt]:
        return [Utt(utterance) for utterance in utterances]




