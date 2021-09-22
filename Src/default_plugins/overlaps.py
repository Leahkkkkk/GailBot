# Standard imports
from typing import Dict, Any, List, Tuple
import re
# Local imports
from Src.default_plugins.turn import Turn
from Src.Components.controller.services import AnalysisPluginInput, \
    AnalysisPlugin, FormatPlugin, FormatPluginInput, Utt

class Overlaps(AnalysisPlugin):
    """
    Combines turns from different sources into a single conversation.
    """

    def __init__(self) -> None:
        ## Vars.
        self.successful = False
        self.marker_limit = 4

    def apply_plugin(self, dependency_outputs : Dict[str,Any],
             plugin_input : AnalysisPluginInput) -> List[Turn]:
        try:
            # Combined turns output
            combined_turns = dependency_outputs["combine_transcripts"]
            overlapped_turns = self._add_overlaps(combined_turns)
            return overlapped_turns
        except:
            pass

    ################################# GETTERS ###############################

    def was_successful(self) -> bool:
        return self.successful

    ############################ PRIVATE METHODS #############################

    def _add_overlaps(self, turns : List[Turn]) -> List[Turn]:
        overlap_turns = list()
        for i in range(len(turns[:-1])):
            current_turn = turns[i]
            next_turn = turns[i+1]
            if current_turn.start_time_seconds > next_turn.end_time_seconds:

                current_x_pos, current_y_pos, next_x_pos, next_y_pos = \
                    self._get_overlap_positions(current_turn, next_turn)
                if abs(current_x_pos - current_y_pos) <= self.marker_limit or \
                        abs(next_x_pos - next_y_pos) <= self.marker_limit:
                    overlap_turns.append(current_turn)
                    continue
                if not re.search('[a-zA-Z]',current_turn.transcript[current_x_pos:current_y_pos]) or \
                        not re.search('[a-zA-Z]',next_turn.transcript[next_x_pos:next_y_pos]):
                    overlap_turns.append(current_turn)
                    continue
                # Adding overlap markers
                new_current_transcript = "{} < {}".format(
                    current_turn.transcript[:current_x_pos],
                    current_turn.transcript[current_x_pos:])
                current_turn.transcript = "{} > [>] {}".format(
                    new_current_transcript[:current_y_pos],
                    new_current_transcript[current_y_pos:]).rstrip()
                new_next_transcript = "{} < {}".format(
                    next_turn.transcript[:next_x_pos],
                    next_turn.transcript[next_x_pos:])
                next_turn.transcript = "{} > [<] ".format(
                    new_next_transcript[:next_y_pos],
                    new_next_transcript[next_y_pos:]).rstrip()
            overlap_turns.append(current_turn)
        overlap_turns.append(turns[-1])
        return overlap_turns

    def _get_overlap_positions(self, current_turn : Turn, next_turn : Turn) \
            -> Tuple:
        return (0,0,0,0)

