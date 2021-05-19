# Standard library imports
from typing import Dict, List
from copy import deepcopy
# Local imports
from ...io import IO
from ...config import Config, SystemBB
# Third party imports

class ConfigService:

    def __init__(self) -> None:
        self.io = IO()
        self.config = Config()
        self.blackboards = {
            "system_blackboard" : None
        }
        self.config_file_path = ""
        self.is_configured = False

    ################################ MODIFIERS ################################
    def configure_from_path(self) -> bool:
        if not self.io.is_file(self.config_file_path):
            return False
        # Read the file and parse it
        success, data = self.io.read(self.config_file_path)
        if not success:
            return False
        return self._parse_config_data(data)

    def reset(self) -> None:
        self.config_file_path = ""
        for bb_type in self.blackboards:
            self.blackboards[bb_type] = None

    ################################ SETTERS ##################################

    def set_configuration_file_path(self, path : str) -> bool:
        if not self.io.is_file(path):
            return False
        self.config_file_path = path
        return True

    ############################## GETTERS ####################################
    def is_fully_configured(self) -> bool:
        for bb_type in self.config.get_blackboard_types():
            if not self.config.get_blackboard(bb_type)[0]:
                return False
        return True

    def get_configuration_file_path(self) -> str:
        return self.config_file_path

    def get_supported_blackboard_types(self) -> List[str]:
        return list(self.config.get_blackboard_types())


    def get_system_blackboard(self) -> SystemBB:
        if self.is_fully_configured():
            return deepcopy(self.blackboards["system_blackboard"])

    ############################# PRIVATE METHODS #############################

    def _parse_config_data(self, data : Dict) -> bool:
        # Data must have all blackboards data.
        if not all([bb_type in data.keys() for bb_type \
                in self.blackboards.keys()]):
            return False
        # Blackboard types must be supported
        if not all([bb_type in self.config.get_blackboard_types() \
                for bb_type in self.blackboards.keys()]):
            return False
        # Load all the blackboards.
        for bb_type in self.blackboards.keys():
            if not self.config.load_blackboard(bb_type,data[bb_type]):
                return False
            loaded, bb = self.config.get_blackboard(bb_type)
            if not loaded:
                return False
            self.blackboards[bb_type] = bb
        return True


