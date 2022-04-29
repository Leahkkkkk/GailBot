# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-02 13:57:50
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-02-17 10:25:19
# Standard imports
from typing import Dict, Any, List, Tuple
import re
from copy import deepcopy
# Local imports
from ...plugins import GBPlugin, PluginMethodSuite, Utt

# TODO: Very ugly code, refactor!


class Overlaps(GBPlugin):

    def __init__(self) -> None:
        super().__init__()
        self.marker_limit = 4

    def apply_plugin(self, dependency_outputs: Dict[str, Any],
                     plugin_input: PluginMethodSuite) -> List[Utt]:
        # Get the output of the previous plugin
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
                if (not re.search('[a-zA-Z]', curr_utt.text[curr_x:curr_y])) or \
                        (not re.search('[a-zA-Z]', nxt_utt.text[nxt_x:nxt_y])):
                    new_utterances.append(curr_utt)
                    continue
                # Add the overlap markers
                curr_utt.text = "{} < {}".format(
                    curr_utt.text[:curr_x],
                    curr_utt.text[curr_x:])
                curr_utt.text = "{} > [>] {}".format(
                    curr_utt.text[:curr_y],
                    curr_utt.text[curr_y:]).rstrip()
                nxt_utt.text = "{} < {}".format(
                    nxt_utt.text[:nxt_x], nxt_utt.text[nxt_x:])
                nxt_utt.text = "{} > [<] {}".format(
                    nxt_utt.text[:nxt_y],
                    nxt_utt.text[nxt_y:]).rstrip()
            new_utterances.append(curr_utt)
        new_utterances.append(utterances[-1])
        self.successful = True
        return new_utterances

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
                start_difference_secs, curr_duration_secs, len(curr_utt.text))
            # Case-1a: In this case, overlap ends at pos y of curr turn and end of nxt turn
            if end_difference_secs > 0:
                pos_y_curr = len(curr_utt.text) - self._calculate_position(
                    end_difference_secs, curr_duration_secs, len(curr_utt.text))
                pos_y_nxt = len(nxt_utt.text)
            # Case-1b: In this case, overlap ends at curr turn end and pos y from turn 2 end.
            elif end_difference_secs < 0:
                pos_y_curr = len(curr_utt.text)
                pos_y_nxt = max(0, len(nxt_utt.text) - self._calculate_position(
                    end_difference_secs, nxt_duration, len(nxt_utt.text)))
            # Case-1c: In this case, overlap ends at both turn ends.
            else:
                pos_y_curr = len(curr_utt.text)
                pos_y_nxt = len(nxt_utt.text)
        elif start_difference_secs < 0:
            pos_x_curr = 0
            pos_x_nxt = self._calculate_position(
                start_difference_secs, nxt_duration, len(nxt_utt.text))
            # Case-2a: In this case, overlap ends at posY from curr turn start and end of nxt turn
            if end_difference_secs > 0:
                pos_y_curr = len(curr_utt.text) - self._calculate_position(
                    end_difference_secs, curr_duration_secs, len(curr_utt.text))
                pos_y_nxt = len(nxt_utt.text)
            # Case-2b: In this case, overlap ends at curr turn ends and posY from nxt turn end.
            elif end_difference_secs < 0:
                pos_y_curr = len(curr_utt.text)
                pos_y_nxt = len(nxt_utt.text) - self._calculate_position(
                    end_difference_secs, nxt_duration, len(nxt_utt.text))
            else:
                pos_y_curr = len(curr_utt.text)
                pos_y_nxt = len(nxt_utt.text)
        # In this case, overlap is from start of both turns.
        else:
            pos_x_curr = 0
            pos_x_nxt = 0
            # Case-3a: In this case, overlap ends at posY from curr turn start and end of nxt turn
            if end_difference_secs > 0:
                pos_y_curr = len(curr_utt.text) - self._calculate_position(
                    end_difference_secs, curr_duration_secs, len(curr_utt.text))
                pos_y_nxt = len(nxt_utt.text)
            # Case-3b: In this case, overlap ends at curr turn ends and posY from nxt turn end.
            elif end_difference_secs < 0:
                pos_y_curr = len(curr_utt.text)
                pos_y_nxt = len(nxt_utt.text) - self._calculate_position(
                    end_difference_secs, nxt_duration, len(nxt_utt.text))
            else:
                pos_y_curr = len(curr_utt.text)
                pos_y_nxt = len(nxt_utt.text)
        # Moving values to start or end of individual turns
        if pos_x_curr >= len(curr_utt.text):
            pos_x_curr = len(curr_utt.text)-1
        if pos_x_nxt >= len(nxt_utt.text):
            pos_x_nxt = len(nxt_utt.text)-1
        if pos_y_curr >= len(curr_utt.text):
            pos_y_curr = len(curr_utt.text)-1
        if pos_y_nxt >= len(nxt_utt.text):
            pos_y_nxt = len(nxt_utt.text)-1
        while curr_utt.text[pos_x_curr] != ' ' and pos_x_curr > 0:
            pos_x_curr -= 1
        while curr_utt.text[pos_y_curr] != ' ' and pos_y_curr < len(curr_utt.text)-1:
            pos_y_curr += 1
        while nxt_utt.text[pos_x_nxt] != ' ' and pos_x_nxt > 0:
            pos_x_nxt -= 1
        while nxt_utt.text[pos_y_nxt] != ' ' and pos_y_nxt < len(nxt_utt.text)-1:
            pos_y_nxt += 1
        if abs(pos_y_curr - len(curr_utt.text)) == 1:
            pos_y_curr += 1
        if abs(pos_y_nxt - len(nxt_utt.text)) == 1:
            pos_y_nxt += 1
        pos_y_curr += 3
        pos_y_nxt += 3
        return pos_x_curr, pos_y_curr, pos_x_nxt, pos_y_nxt

    def _calculate_position(self, difference_secs, duration_secs,
                            textion_length):
        return int(
            round((((abs(difference_secs)/duration_secs))*textion_length)))
