# Standard library imports
from typing import Dict, List
from copy import deepcopy
# Local imports
from ....io import IO
from ....config import Config, SystemBB
from ..fs_service import FileSystemService

class ConfigService:


    def __init__(self, fs_service : FileSystemService) -> None:
        self.fs_service = fs_service
        self.io = IO()
        self.config = Config()
        self.blackboards = {
            "system_blackboard" : None
        }

    ################################ MODIFIERS ################################

    def configure_from_path(self) -> bool:
        try:
            return self._parse_config_data(
                self.fs_service.get_config_service_data_from_disk())
        except:
            return False

    ############################## GETTERS ####################################

    def is_configured(self) -> bool:
        for bb_type in self.config.get_blackboard_types():
            if not self.config.get_blackboard(bb_type)[0]:
                return False
        return True

    def get_configuration_file_path(self) -> str:
        return self.fs_service.get_config_service_configuration_source()

    def get_supported_blackboard_types(self) -> List[str]:
        return list(self.config.get_blackboard_types())

    def get_system_blackboard(self) -> SystemBB:
        if self.is_configured():
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