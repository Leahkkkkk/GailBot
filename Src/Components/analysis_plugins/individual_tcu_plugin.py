# Standard imports
from typing import Dict, Any, List
# Local imports
from Src.Components.controller.services import AnalysisPluginInput, \
    AnalysisPlugin, Utt
from Src.default_plugins.analysis_plugins.turn import Turn


class SourceTCUAnalysis(AnalysisPlugin):

    def __init__(self) -> None:
        pass

    def apply_plugin(self, dependency_outputs : Dict[str,Any],
             plugin_input : AnalysisPluginInput) -> Any:
        pass

    def was_successful(self) -> bool:
        pass



# class TCUAnalysis(AnalysisPlugin):
#     """
#     Constructs Turns for individual source files.
#     """

#     def __init__(self) -> None:
#         ## Vars.
#         self.is_successful = False
#         self.turn_end_threshold_seconds = 0.1

#     def apply_plugin(self, dependency_outputs : Dict[str,Any],
#             plugin_input : AnalysisPluginInput) -> Any:
#         try:
#             utterance_map = plugin_input.get_utterances()
#             # Convert utterances to turn objects.
#             turn_map = self._utterancesack_to_turns(utterance_map)
#             # Use turn map to construct source tcu's per source file.
#             tcu_map = self._construct_tcu_map(turn_map)
#             # Combine turn map into a single conversation.
#             combined_tcus = self._squeeze_turn_map(tcu_map)
#             # Print
#             #self._print_tcu_map(tcu_map)
#             #self._print_tcus(combined_tcus)
#             self.is_successful = True
#             return combined_tcus
#         except Exception as e:
#             print(e)

#     def was_successful(self) -> bool:
#         return self.is_successful

#     ############################## PRIVATE METHODS ###########################

#     def _print_tcu_map(self, tcu_map : Dict[str,Turn]) -> None:
#         for tcus in tcu_map.values():
#             self._print_tcus(tcus)

#     def _print_tcus(self, tcus : List[Turn]) -> None:
#         for tcu in tcus:
#             print("{}: {} {}_{}".format(
#                 tcu.speaker,tcu.transcript,tcu.start_time_seconds,
#                 tcu.end_time_seconds))

#     def _utterances_to_turns(self, utterance_map : Dict[str,List[Utt]]) \
#             -> Dict[str,List[Turn]]:
#         turns_map = dict()
#         for source_name, utterances in utterance_map.items():
#             turns = list()
#             for utt in utterances:
#                 turn = Turn(
#                     utt.get_speaker_label(), utt.get_start_time_seconds(),
#                     utt.get_end_time_seconds(), utt.get_transcript())
#                 turns.append(turn)
#             turns_map[source_name] = turns
#         return turns_map

#     def _construct_tcu_map(self, turn_map : Dict[str,List[Turn]]) \
#             -> Dict[str,List[Turn]]:
#         tcu_map = dict()
#         for source_name, turns in turn_map.items():
#             tcus = self._construct_tcu_from_turns(turns)
#             tcu_map[source_name] = tcus
#         return tcu_map

#     def _construct_tcu_from_turns(self, turns : List[Turn]) -> List[Turn]:
#         tcus = turns
#         count = 0
#         while count < len(tcus) - 1:
#             current_turn = tcus[count]
#             next_turn = tcus[count+1]
#             if ((next_turn.start_time_seconds - current_turn.end_time_seconds) <= \
#                         self.turn_end_threshold_seconds) and \
#                     next_turn.speaker == current_turn.speaker:
#                 new_turn = Turn(
#                     current_turn.speaker, current_turn.start_time_seconds,
#                     next_turn.end_time_seconds,"{} {}".format(
#                         current_turn.transcript,next_turn.transcript))
#                 tcus[count] = new_turn
#                 del tcus[count + 1]
#             else:
#                 count += 1
#         return tcus

#     def _squeeze_turn_map(self, turn_map : Dict[str,Turn]) -> List[Turn]:
#         combined_turns = list()
#         # Add all turns into combined list.
#         for source_name, turns in turn_map.items():
#             combined_turns.extend(turns)
#         # Sort the combined list using start times.
#         combined_turns.sort(key=lambda turn: turn.start_time_seconds)
#         tcus = self._construct_tcu_from_turns(combined_turns)
#         return tcus







