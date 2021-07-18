# Standard imports
from typing import Any, Dict, List
from dataclasses import dataclass
# Local imports
from ....config import ConfigLoader, BlackBoard

@dataclass
class SystemBlackBoard(BlackBoard):
    """
    Contains system configurations.
    """
    engine_type : str
    watson_api_key : str
    watson_language_customization_id : str
    watson_base_language_model : str
    watson_region : str
    analysis_plugins_to_apply : List[str]
    output_format : str

class SystemBlackBoardLoader(ConfigLoader):

    def __init__(self) -> None:
        pass

    ############################### MODIFIERS #################################

    def load_blackboard(self, blackboard_data : Dict[str,Dict]) \
            -> SystemBlackBoard:
        return self._parse_configuration_data(blackboard_data)

    ############################## PRIVATE METHODS #############################

    def _parse_configuration_data(self, blackboard_data : Dict[str,Dict]) \
            -> SystemBlackBoard:
        """
        Expected data format: {
            {
                key-value pairs are as defined below.
            }
        }
        """
        # Expects dictionary of dictionaries.
        if not type(blackboard_data) == dict:
            return
        if not all(type(v) == dict for v in blackboard_data.values()):
            return
        try:
            settings = blackboard_data["default_settings_profile"]
            return SystemBlackBoard(
                settings["engine_type"],
                settings["watson_api_key"],
                settings["watson_language_customization_id"],
                settings["watson_base_language_model"],
                settings["watson_region"],
                settings["analysis_plugins_to_apply"],
                settings["output_format"])
        except:
            pass
