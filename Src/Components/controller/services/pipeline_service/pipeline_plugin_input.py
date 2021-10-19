# Standard imports
from typing import Any, Dict, List
from copy import deepcopy
# Local imports
from ....engines import Utterance, UtteranceAttributes
from .plugin_utterance_wrapper import Utt
from .pipeline_payload import SourcePayload


class PipelinePluginInput:
    """
    Provides basic methods that can be passed to a plugin added to the pipeline
    service. Usually subclassed to add specifalized method for specific type
    of plugins.
    """

    def __init__(self, payload: SourcePayload) -> None:
        """
        Args:
            payload (SourcePayload)
        """
        self.payload = payload
    ################################# MODIFIERS ###############################

    def add_to_source(self, identifier: str, path: str,
                      copy: bool = False) -> bool:
        """
        Add an item with the specified identifier and path to the output
        for the specific source.

        Args:
            identifier (str): Unique identifier for the file or directory.
            path (str): Path to a file or directory.
            copy (bool):
                If True, copies the file or directory, otherwise moves the
                file or directory.

        Returns:
            (bool): True if the item is successfully added, False otherwise.
        """
        return self.payload.add_to_source(
            identifier, path, "permanent", copy)

    def write_to_file(self, identifier: str, file_name: str,
                      extension: str, data: Any, overwrite: bool = False) -> bool:
        """
        Write a file with the specified identifier, file_name, extension,
        and data to the results for this specific source.

        Args:
            identifier (str): Unique identifier for the file or directory.
            file_name (str): Name of the file.
            extension (str): Extension of the file.
            overwrite (bool): If True, any existing file with the same name
                            or extension is overwritten.

        Returns:
            (bool): True if successfully written, False otherwise.
        """
        return self.payload.write_to_file(
            identifier, "permanent", file_name, extension, data, overwrite)

    ################################# GETTERS ###############################

    def get_source_name(self) -> str:
        """
        Obtain the name of the source
        """
        return self.payload.get_source_name()

    def get_workspace_path(self) -> str:
        """
        Obtain a path to a workspace that can be used as a space to write
        extra objects for this source.
        """
        return self.payload.get_workspace_path()

    def result_directory_path(self) -> str:
        """
        Obtain the path to the result directory for this source.
        """
        return self.payload.get_result_directory_path()

    def get_utterances(self) -> Dict[str, List[Utt]]:
        """
        Obtain a mapping from the source file name to its utterances.

        Returns:
            (Dict[str,List[Utt]])
        """
        utterances_wrap_map = dict()
        utterance_map = self.payload.get_conversation().get_utterances()
        for name, utterances in utterance_map.items():
            utterances_wrap_map[name] = self._wrap_utterances(
                utterances)
        return utterances_wrap_map

    def get_source_paths(self) -> Dict[str, str]:
        """
        Obtain a mapping from the name of a source file to its paths, for this
        particular source.

        Returns:
            (Dict[str,str])
        """
        return self.payload.get_conversation().get_source_file_paths()

    ############################# PRIVATE METHODS ###########################

    def _wrap_utterances(self, utterances: List[Utterance]) -> List[Utt]:
        return [self._wrap_utterance(utterance) for utterance in utterances]

    def _wrap_utterance(self, utterance: Utterance) -> Utt:
        utt = Utt()
        utt.speaker_label = utterance.get(UtteranceAttributes.speaker_label)[1]
        utt.start_time_seconds = utterance.get(
            UtteranceAttributes.start_time)[1]
        utt.end_time_seconds = utterance.get(UtteranceAttributes.end_time)[1]
        utt.transcript = utterance.get(UtteranceAttributes.transcript)[1]
        return utt
