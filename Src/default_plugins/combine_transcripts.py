# Standard imports
from typing import Dict, Any, List
# Local imports
from Src.default_plugins.turn import Turn
from Src.Components.controller.services import AnalysisPluginInput, \
    AnalysisPlugin, FormatPlugin, FormatPluginInput, Utt

class CombineTranscripts(AnalysisPlugin):
    """
    Combines turns from different sources into a single conversation.
    """

    def __init__(self) -> None:
        ## Vars.
        self.successful = False

    def apply_plugin(self, dependency_outputs : Dict[str,Any],
             plugin_input : AnalysisPluginInput) -> List[Turn]:
        try:
            # Individual turns output
            turns_map = dependency_outputs["individual_turns"]
            turns = list()
            for individual_turns in turns_map.values():
                turns.extend(individual_turns)
            turns.sort(lambda turn: turn.start_time_seconds)
            self.successful = True
            return turns
        except:
            pass

    ################################# GETTERS ###############################

    def was_successful(self) -> bool:
        return self.successful

    ############################ PRIVATE METHODS #############################
