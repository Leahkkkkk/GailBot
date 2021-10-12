# Standard library imports
# Local imports
from ....io import IO
from ....config import Config
from ..fs_service import FileSystemService
from .system_bb_loader import SystemBlackBoard, SystemBlackBoardLoader


class ConfigService:

    def __init__(self, fs_service: FileSystemService) -> None:
        # Vars.
        self.system_blackboard: SystemBlackBoard = None
        # Objects
        self.fs_service = fs_service
        self.io = IO()
        self.config = Config()
        # Add loaders to the config service.
        self.config.add_loader(SystemBlackBoardLoader())
        self._load_blackboards()

    ############################# MODIFIERS ##################################

    ############################# GETTERS ####################################

    def is_configured(self) -> bool:
        """
        Determine whether the service is configured i.e., all blackboards are
        loaded.

        Returns:
            (bool): True if the service is configured, False otherwise.
        """
        return self.system_blackboard != None

    def get_system_blackboard(self) -> SystemBlackBoard:
        """
        Obtain the system blackboard.

        Returns:
            (SystemBlackBoard)
        """
        return self.system_blackboard

    ########################## PRIVATE METHODS ###############################

    def _load_blackboards(self) -> None:
        """
        Load all blackboards.
        """
        try:
            # Load System BB
            self.system_blackboard = self.config.load_blackboard(
                self.fs_service.get_system_blackboard_configuration_data())
        except:
            raise Exception("ConfigService loader error")
