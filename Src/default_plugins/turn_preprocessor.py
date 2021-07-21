# Standard imports
from typing import Dict, Any, List
# Local imports
from Src.default_plugins.turn import Turn
from Src.Components.controller.services import AnalysisPluginInput, \
    AnalysisPlugin, FormatPlugin, FormatPluginInput, Utt

class TurnPreprocessor(AnalysisPlugin):
    """
    Preprocesses every Utt into a Turn object for use with analysis plugins.
    """

    def __init__(self) -> None:
        self.successful = False

    def apply_plugin(self, dependency_outputs : Dict[str,Any],
             plugin_input : AnalysisPluginInput) -> Any:
        turns_map = dict()
        utterance_map = plugin_input.get_utterances()
        for source_name , utterances in utterance_map.items():
            turns = self._generate_turns(utterances)
            turns_map[source_name] = turns
        self.successful = True
        return turns_map

    def was_successful(self) -> bool:
        return self.successful

    def _generate_turns(self, utterances : List[Utt]) -> List[Turn]:
        turns = list()
        for i,utt in enumerate(utterances):
            turn = Turn(
                utt.speaker_label,utt.start_time_seconds,utt.end_time_seconds,
                utt.transcript)
            turns.append(turn)
        return turns

