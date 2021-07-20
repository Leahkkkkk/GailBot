# Standard imports
from typing import Dict, Any, List
import re
# Local imports
from Src.Components.controller.services import AnalysisPluginInput, \
    AnalysisPlugin, Utt
from Src.default_plugins.analysis_plugins.turn import Turn

class OverlapAnalysis(AnalysisPlugin):
    """
    Constructs Turns for individual source files.
    """

    def __init__(self) -> None:
        ## Vars.
        self.is_successful = False
        self.marker_limit = 4

    def apply_plugin(self, dependency_outputs : Dict[str,Any],
            plugin_input : AnalysisPluginInput) -> Any:
        try:
            combined_turns = dependency_outputs["tcu"]
            overlap_tcus =  self._generate_overlaps(combined_turns)
            self._print_tcus(overlap_tcus)
        except Exception as e:
            print(e)

    def was_successful(self) -> bool:
        return self.is_successful

    ############################## PRIVATE METHODS ###########################

    def _print_tcus(self, tcus : List[Turn]) -> None:
        for tcu in tcus:
            print("{}: {} {}_{}".format(
                tcu.speaker,tcu.transcript,tcu.start_time_seconds,
                tcu.end_time_seconds))

    def _generate_overlaps(self, tcus : List[Turn]) -> List[Turn]:
        overlap_tcus = tcus
        for i in range(len(tcus)):
            current_tcu = tcus[i]
            next_tcu = tcus[i+1]
            current_x_pos, current_y_pos, next_x_pos, next_y_pos = \
                self._get_overlap_positions(current_tcu, next_tcu)
            if abs(current_x_pos - current_y_pos) <= self.marker_limit or \
                    abs(next_x_pos - next_y_pos) <= self.marker_limit:
                overlap_tcus.append(current_tcu)
                continue
            if not re.search('[a-zA-Z]',current_tcu.transcript[current_x_pos:current_y_pos]) or \
                    not re.search('[a-zA-Z]',next_tcu.transcript[next_x_pos:next_y_pos]):
                overlap_tcus.append(current_tcu)
                continue
            new_current_transcript = "{} < {}"


    def _get_overlap_positions(self, current_tcu : Turn, next_tcu : Turn) \
            -> Dict[str,int]:
        pass

