# Standard imports
from typing import Dict, Any, List
from dataclasses import dataclass, field
from copy import deepcopy
# Local imports
from Src.default_plugins.turn import Turn
from Src.Components.controller.services import AnalysisPluginInput, \
    AnalysisPlugin, FormatPlugin, FormatPluginInput, Utt


class IndividualTurns(AnalysisPlugin):
    """
    Construct individual turns.
    """

    def __init__(self) -> None:
        ## Vars.
        self.successful = False
        self.turn_end_threshold_seconds = 0.1

    ################################# MODIFIERS #############################

    def apply_plugin(self, dependency_outputs : Dict[str,Any],
             plugin_input : AnalysisPluginInput) -> Dict[str,List[Turn]]:
        try:
            # Obtain output from dependencies
            turns_map : Dict[str,List[Turn]] = \
               dependency_outputs["turn_preprocessor"]
            speaker_turns_map : Dict[str,List[Turn]] = dict()
            for source_name, word_level_turns in turns_map.items():
               # Create word level individual speaker turns
               speaker_turns_map[source_name] = self._construct_speaker_turns(
                   deepcopy(word_level_turns))
            return speaker_turns_map
        except:
            pass

    ################################# GETTERS ###############################

    def was_successful(self) -> bool:
        return self.successful

    ############################ PRIVATE METHODS #############################

    def _construct_speaker_turns(self, word_level_turns : List[Turn]) \
            -> List[Turn]:
        turns = deepcopy(word_level_turns)
        count = 0
        while count < len(turns) -1:
            current_turn = turns[count]
            next_turn = turns[count+1]
            fto = next_turn.start_time_seconds - current_turn.end_time_seconds
            if fto <= self.turn_end_threshold_seconds and \
                    next_turn.speaker_label == current_turn.speaker_label:
                new_transcript = "{} {}".format(
                    current_turn.transcript, next_turn.transcript)
                # Update the turn
                current_turn.end_time_seconds = next_turn.end_time_seconds
                current_turn.transcript = new_transcript
                del turns[count+1]
            else:
                count += 1
        return turns




