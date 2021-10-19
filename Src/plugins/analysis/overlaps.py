# Standard imports
from typing import Dict, Any, List, Tuple
import re
from copy import deepcopy
# Local imports
from Src.default_plugins.turn import Turn
from Src.Components.controller.services import AnalysisPluginInput, \
    AnalysisPlugin, Utt

# TODO: Very ugly code, refactor!


class Overlaps(AnalysisPlugin):

    def __init__(self) -> None:
        self.marker_limit = 4

    def apply_plugin(self, dependency_outputs: Dict[str, Any],
                     plugin_input: AnalysisPluginInput) -> List[Turn]:
        # Get the output of the previous plugin
        try:
            utterances: List[Utt] = dependency_outputs["combine_turns"]
            new_utterances = list()
            for i, curr_utt in enumerate(utterances[:-1]):
                curr_utt = deepcopy(curr_utt)
                nxt_utt = deepcopy(utterances[i+1])
                # In this case there is some overlap
                if curr_utt.end_time_seconds - nxt_utt.start_time_seconds:
                    curr_x, curr_y, nxt_x, nxt_y = self._get_overlap_positions(
                        curr_utt, nxt_utt)
                    if (abs(curr_x - curr_y) <= self.marker_limit) or \
                            (abs(nxt_x - nxt_y) <= self.marker_limit):
                        new_utterances.append(curr_utt)
                        continue
                    # Not adding markers if there is no character within limit
                    # Not adding markers encompassing comments.
                    if (not re.search('[a-zA-Z]', curr_utt.transcript[curr_x:curr_y])) or \
                            (not re.search('[a-zA-Z]', nxt_utt.transcript[nxt_x:nxt_y])):
                        new_utterances.append(curr_utt)
                        continue
                    # Add the overlap markers
                    curr_utt.transcript = "{} < {}".format(
                        curr_utt.transcript[:curr_x],
                        curr_utt.transcript[curr_x:])
                    curr_utt.transcript = "{} > [>] {}".format(
                        curr_utt.transcript[:curr_y],
                        curr_utt.transcript[curr_y:]).rstrip()
                    nxt_utt.transcript = "{} < {}".format(
                        nxt_utt.transcript[:nxt_x], nxt_utt.transcript[nxt_x:])
                    nxt_utt.transcript = "{} > [<] {}".format(
                        nxt_utt.transcript[:nxt_y],
                        nxt_utt.transcript[nxt_y:]).rstrip()
                new_utterances.append(curr_utt)
            new_utterances.append(utterances[-1])
            return new_utterances
        except Exception as e:
            print(e)

        ################################# GETTERS ###############################

    def was_successful(self) -> bool:
        return True

    def _get_overlap_positions(self, curr_utt: Utt, nxt_utt: Utt) -> Tuple:
        start_difference_secs = \
            nxt_utt.start_time_seconds - curr_utt.start_time_seconds
        end_difference_secs = curr_utt.end_time_seconds - nxt_utt.end_time_seconds
        curr_duration_secs = curr_utt.end_time_seconds - curr_utt.start_time_seconds
        nxt_duration = nxt_utt.end_time_seconds - nxt_utt.start_time_seconds
        # In this case, the overlap is at nxt start and pos x of curr turn.
        if start_difference_secs > 0:
            pos_x_nxt = 0
            pos_x_curr = self._calculate_position(
                start_difference_secs, curr_duration_secs, len(curr_utt.transcript))
            # Case-1a: In this case, overlap ends at pos y of curr turn and end of nxt turn
            if end_difference_secs > 0:
                pos_y_curr = len(curr_utt.transcript) - self._calculate_position(
                    end_difference_secs, curr_duration_secs, len(curr_utt.transcript))
                pos_y_nxt = len(nxt_utt.transcript)
            # Case-1b: In this case, overlap ends at curr turn end and pos y from turn 2 end.
            elif end_difference_secs < 0:
                pos_y_curr = len(curr_utt.transcript)
                pos_y_nxt = max(0, len(nxt_utt.transcript) - self._calculate_position(
                    end_difference_secs, nxt_duration, len(nxt_utt.transcript)))
            # Case-1c: In this case, overlap ends at both turn ends.
            else:
                pos_y_curr = len(curr_utt.transcript)
                pos_y_nxt = len(nxt_utt.transcript)
        elif start_difference_secs < 0:
            pos_x_curr = 0
            pos_x_nxt = self._calculate_position(
                start_difference_secs, nxt_duration, len(nxt_utt.transcript))
            # Case-2a: In this case, overlap ends at posY from curr turn start and end of nxt turn
            if end_difference_secs > 0:
                pos_y_curr = len(curr_utt.transcript) - self._calculate_position(
                    end_difference_secs, curr_duration_secs, len(curr_utt.transcript))
                pos_y_nxt = len(nxt_utt.transcript)
            # Case-2b: In this case, overlap ends at curr turn ends and posY from nxt turn end.
            elif end_difference_secs < 0:
                pos_y_curr = len(curr_utt.transcript)
                pos_y_nxt = len(nxt_utt.transcript) - self._calculate_position(
                    end_difference_secs, nxt_duration, len(nxt_utt.transcript))
            else:
                pos_y_curr = len(curr_utt.transcript)
                pos_y_nxt = len(nxt_utt.transcript)
        # In this case, overlap is from start of both turns.
        else:
            pos_x_curr = 0
            pos_x_nxt = 0
            # Case-3a: In this case, overlap ends at posY from curr turn start and end of nxt turn
            if end_difference_secs > 0:
                pos_y_curr = len(curr_utt.transcript) - self._calculate_position(
                    end_difference_secs, curr_duration_secs, len(curr_utt.transcript))
                pos_y_nxt = len(nxt_utt.transcript)
            # Case-3b: In this case, overlap ends at curr turn ends and posY from nxt turn end.
            elif end_difference_secs < 0:
                pos_y_curr = len(curr_utt.transcript)
                pos_y_nxt = len(nxt_utt.transcript) - self._calculate_position(
                    end_difference_secs, nxt_duration, len(nxt_utt.transcript))
            else:
                pos_y_curr = len(curr_utt.transcript)
                pos_y_nxt = len(nxt_utt.transcript)
        # Moving values to start or end of individual turns
        if pos_x_curr >= len(curr_utt.transcript):
            pos_x_curr = len(curr_utt.transcript)-1
        if pos_x_nxt >= len(nxt_utt.transcript):
            pos_x_nxt = len(nxt_utt.transcript)-1
        if pos_y_curr >= len(curr_utt.transcript):
            pos_y_curr = len(curr_utt.transcript)-1
        if pos_y_nxt >= len(nxt_utt.transcript):
            pos_y_nxt = len(nxt_utt.transcript)-1
        while curr_utt.transcript[pos_x_curr] != ' ' and pos_x_curr > 0:
            pos_x_curr -= 1
        while curr_utt.transcript[pos_y_curr] != ' ' and pos_y_curr < len(curr_utt.transcript)-1:
            pos_y_curr += 1
        while nxt_utt.transcript[pos_x_nxt] != ' ' and pos_x_nxt > 0:
            pos_x_nxt -= 1
        while nxt_utt.transcript[pos_y_nxt] != ' ' and pos_y_nxt < len(nxt_utt.transcript)-1:
            pos_y_nxt += 1
        if abs(pos_y_curr - len(curr_utt.transcript)) == 1:
            pos_y_curr += 1
        if abs(pos_y_nxt - len(nxt_utt.transcript)) == 1:
            pos_y_nxt += 1
        pos_y_curr += 3
        pos_y_nxt += 3
        return pos_x_curr, pos_y_curr, pos_x_nxt, pos_y_nxt

    def _calculate_position(self, difference_secs, duration_secs,
                            transcription_length):
        return int(
            round((((abs(difference_secs)/duration_secs))*transcription_length)))
