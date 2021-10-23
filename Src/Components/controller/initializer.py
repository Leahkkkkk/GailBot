from typing import Tuple, Dict, List, Any
from dataclasses import dataclass

from ..io import IO
from ..config import Config
from ..services import FileSystemService, OrganizerService
from .helpers.gb_settings import GailBotSettings, GBSettingAttrs
from .pipeline import GBPipeline
from .pipeline import Utt
from .blackboards import PipelineConfigLoader, PipelineBlackBoard,\
    ServicesBlackBoard, ServicesConfigLoader

# -------------- Initializer


@dataclass
class BlackBoards:
    pipeline_blackboard: PipelineBlackBoard
    services_blackboard: ServicesBlackBoard


@ dataclass
class Services:

    fs_service: FileSystemService = None
    organizer_service: OrganizerService = None
    pipeline: GBPipeline = None
    is_initialized: bool = False
    blackboards: BlackBoards = None


class GBInitializer:

    # TODO: For now, all the blackboard cars are defined here but they
    # should come from a file.

    DEFAULT_SETTINGS_TYPE = "gb"
    RAW_EXTENSION = "gb"
    METADATA_EXTENSION = "json"
    METADATA_NAME = "metadata"
    DEFAULT_SETTINGS_TYPE = "gb"

    def __init__(self, ws_dir_path: str) -> None:
        self.io = IO()
        # Config initialize and loading blackboards
        self.config = Config()
        self.config.add_loader(PipelineConfigLoader())
        self.config.add_loader(ServicesConfigLoader())
        pipeline_blackboard = self.config.load_blackboard({
            "raw_extension": self.RAW_EXTENSION,
            "metadata_name": self.METADATA_NAME,
            "metadata_extension": self.METADATA_EXTENSION
        })
        services_blackboard = self.config.load_blackboard({
            "default_settings_type": self.DEFAULT_SETTINGS_TYPE
        })
        # Fs service initialize
        fs_service = FileSystemService()
        configured = fs_service.configure_from_workspace_path(ws_dir_path)
        # Organizer service initialize
        organizer_service = OrganizerService(fs_service)
        organizer_service.set_conversation_creator_method(
            self._conversation_creator_method)
        profile_added = organizer_service.add_settings_profile_type(
            self.DEFAULT_SETTINGS_TYPE, lambda data: GailBotSettings(data))
        # pipeline initialize
        pipeline = GBPipeline(pipeline_blackboard)
        # Checking if fully configured
        if configured and profile_added:
            self.services = Services(
                fs_service, organizer_service, pipeline, True,
                BlackBoards(pipeline_blackboard, services_blackboard))
        else:
            self.services = Services()

    ############################# MODIFIERS ###############################

    def initialize(self) -> Services:
        return self.services

    ########################### PRIVATE METHODS ############################

    def _conversation_creator_method(self, source_path: str) -> List[Dict]:
        data_file_configs = list()
        if self.io.is_file(source_path):
            data_file_configs.append(
                self._create_data_file_config(source_path))
        else:
            supported_formats = list(self.io.get_supported_audio_formats())
            supported_formats.extend(
                list(self.io.get_supported_video_formats()))
            # NOTE: Check - adding additional gb_raw format to look for
            supported_formats.append("gb")
            _, file_paths = self.io.path_of_files_in_directory(
                self.source_path, supported_formats, False)
            for path in file_paths:
                data_file_configs.append(
                    self._create_data_file_config(path))
        return data_file_configs

    def _create_data_file_config(self, source_file_path: str) -> Dict:
        configs = dict()
        utterances = list()
        if not self.io.is_file(source_file_path):
            raise Exception()
        if self.io.is_supported_audio_file(source_file_path):
            file_type = "audio"
        elif self.io.is_supported_video_file(source_file_path):
            file_type = "video"
        # -- NOTE: Check - assing handler for gb_raw file here!
        elif self.io.get_file_extension(source_file_path)[1] == self.RAW_EXTENSION:
            # Parse the raw file
            # NOTE: The data file type needs to be changes / added maybe?
            file_type = "audio"
            data = open(source_file_path, "r").readlines()
            for line in data:
                tokens = line.split(" ")
                utt = Utt(
                    tokens[0].rstrip(":"),
                    float(tokens[2][:tokens[2].find("_")]),
                    float(tokens[2][tokens[2].find("_")+1:].rstrip("/n")),
                    tokens[1])
                utterances.append(utt)
        else:
            raise Exception()
        return {
            "name": self.io.get_name(source_file_path),
            "extension": self.io.get_file_extension(source_file_path)[1],
            "file_type": file_type,
            "path": source_file_path,
            "size_bytes":  self.io.get_size(source_file_path)[1],
            "utterances": utterances
        }
