from typing import Tuple, Dict, List, Any
from dataclasses import dataclass

from Src.components.services import fs_service
from ..io import IO
from ..config import Config
from ..services import FileSystemService, OrganizerService
from .helpers.gb_settings import GailBotSettings, GBSettingAttrs
from .pipeline import GBPipeline, Utt, Payload, ExternalMethods
from .blackboards import PipelineConfigLoader, PipelineBlackBoard,\
    ServicesBlackBoard, ServicesConfigLoader
from ..organizer import Conversation
from ..services import Source

# --------------- Models


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

    # TODO: THese should not be hard-coded here.
    DEFAULT_SETTINGS_TYPE = "gb"
    RAW_EXTENSION = "gb"
    METADATA_EXTENSION = "json"
    METADATA_NAME = "metadata"
    DEFAULT_SETTINGS_TYPE = "gb"

    def __init__(self) -> None:
        # -- Objects
        self.io = IO()
        self.config = Config()
        self.config.add_loader(PipelineConfigLoader())
        self.config.add_loader(ServicesConfigLoader())

    ############################# MODIFIERS ###############################

    def initialize(self, ws_dir_path: str) -> Services:
        blackboards = self._load_blackboards(ws_dir_path)
        fs_service = self._initialize_fs_service(ws_dir_path)
        organizer_service = self._initialize_organizer_service(
            ws_dir_path, fs_service)
        pipeline_service = self._initialize_pipeline_service(
            ws_dir_path, blackboards)
        return Services(
            fs_service, organizer_service, pipeline_service, True, blackboards)

    ############################# PRIVATE METHODS ##########################

    def _load_blackboards(self, ws_dir_path: str) -> BlackBoards:
        # TODO: For now, use the hard-coded variables
        pipeline_blackboard = self.config.load_blackboard({
            "raw_extension": self.RAW_EXTENSION,
            "metadata_name": self.METADATA_NAME,
            "metadata_extension": self.METADATA_EXTENSION
        })
        services_blackboard = self.config.load_blackboard({
            "default_settings_type": self.DEFAULT_SETTINGS_TYPE
        })
        return BlackBoards(pipeline_blackboard, services_blackboard)

    def _initialize_fs_service(self, ws_dir_path: str) -> FileSystemService:
        fs_service = FileSystemService()
        configured = fs_service.configure_from_workspace_path(ws_dir_path)
        if not configured:
            raise Exception("Fs_service cannot be initialized")
        return fs_service

    def _initialize_organizer_service(
            self, ws_dir_path: str, fs_service: FileSystemService) \
            -> OrganizerService:
        organizer_service = OrganizerService(fs_service)
        organizer_service.set_conversation_creator_method(
            self.create_conversation)
        organizer_service.add_source_can_load_method(
            self.can_load_file_source)
        organizer_service.add_source_can_load_method(
            self.can_load_directory_source)
        organizer_service.add_source_can_load_method(
            self.can_load_transcribed_source)
        profile_added = organizer_service.add_settings_profile_type(
            self.DEFAULT_SETTINGS_TYPE, lambda data: GailBotSettings(data))
        if not profile_added:
            raise Exception("Organizer service cannot be initialized")
        return organizer_service

    def _initialize_pipeline_service(
            self, ws_dir_path: str, blackboards: BlackBoards) -> GBPipeline:
        methods = ExternalMethods(
            self.create_payload, self.create_metadata)
        pipeline = GBPipeline(
            blackboards.pipeline_blackboard, methods)
        return pipeline

    # ----------------------------- CONFIGURATION METHODS

    # -- Type 1: Checkers for organizer SourceLoader

    def can_load_file_source(self, source_path: str) -> bool:
        # Must be file.
        if not self.io.is_file(source_path):
            return False
        # Must be supported.
        _, source_extension = self.io.get_file_extension(source_path)
        if not source_extension in self.io.get_supported_audio_formats() and \
                not source_extension in self.io.get_supported_video_formats():
            return False
        return True

    def can_load_directory_source(self, source_path: str) -> bool:
        return self.io.is_directory(source_path)

    def can_load_transcribed_source(self, source_path: str) -> bool:
        if not self.io.is_directory(source_path):
            return False
        # Check if the metadata file exists
        if not self._does_meta_exist(source_path):
            return False
        # Read the metatafile and use it to check other files
        meta_path = self._get_meta_path(source_path)
        did_read, meta_data = self.io.read(meta_path)
        if meta_path == None or not did_read:
            return False
        try:
            # The data should have been transcribed properly and
            # raw files should be there.
            return meta_data["is_transcribed"] and \
                self._check_raw_outputs(source_path, meta_data["outputs"])
        except Exception as e:
            return False

    # -- Type 2: PipelineService methods

    def create_payload(self, source: Source) -> None:
        return Payload(source)

    def create_metadata(self, payload: Payload) -> Dict:
        pass

    # -- Type 3: Conversation creator methods

    def create_conversation(self, source_path: str) -> List[Dict]:
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
                source_path, supported_formats, False)
            for path in file_paths:
                data_file_configs.append(
                    self._create_data_file_config(path))
        return data_file_configs

    # Type 4: Helpers

    def check_raw_outputs(
            self, source_path,  output_paths: List[str]) -> bool:
        raw_outputs = [path for path in output_paths if
                       self.io.get_file_extension(path)
                       == self.source_raw_transcription_extension]
        # Ensure that this matches the actual raw files.
        _, actual_paths = self.io.path_of_files_in_directory(
            source_path, [self.source_raw_transcription_extension], False)
        actual_names = [self.io.get_name(
            path) for path in actual_paths]
        for raw_output in raw_outputs:
            if not self.io.get_name(raw_output) in actual_names:
                return False
        return True

    def _get_meta_path(self, source_path: str) -> str:
        _, paths = self.io.path_of_files_in_directory(
            source_path, [self.METADATA_EXTENSION], False)
        return [path for path in paths if self.io.get_name(
            path) == self.metadata_file_name][0]

    def _does_meta_exist(self, source_path: str) -> bool:
        _, paths = self.io.path_of_files_in_directory(
            source_path, [self.METADATA_EXTENSION], False)
        return len([path for path in paths if self.io.get_name(
            path) == self.metadata_file_name]) > 0

    def _create_data_file_config(self, source_file_path: str) -> Dict:
        # configs = dict()
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
                # NOTE: This split delimiter should also be in the
                # blackboard.
                tokens = line.split(",")
                utt = Utt(
                    tokens[0],
                    float(tokens[2]),
                    float(tokens[3]),
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


# # -------------- Initializer


# class GBInitializer:

#     # TODO: THese should not be hard-coded here.
#     DEFAULT_SETTINGS_TYPE = "gb"
#     RAW_EXTENSION = "gb"
#     METADATA_EXTENSION = "json"
#     METADATA_NAME = "metadata"
#     DEFAULT_SETTINGS_TYPE = "gb"

#     def __init__(self, ws_dir_path: str) -> None:
#         self.io = IO()
#         # Config initialize and loading blackboards
#         self.config = Config()
#         self.config.add_loader(PipelineConfigLoader())
#         self.config.add_loader(ServicesConfigLoader())
#         pipeline_blackboard = self.config.load_blackboard({
#             "raw_extension": self.RAW_EXTENSION,
#             "metadata_name": self.METADATA_NAME,
#             "metadata_extension": self.METADATA_EXTENSION
#         })
#         services_blackboard = self.config.load_blackboard({
#             "default_settings_type": self.DEFAULT_SETTINGS_TYPE
#         })
#         # FsService Initialize
#         fs_service = FileSystemService()
#         configured = fs_service.configure_from_workspace_path(ws_dir_path)
#         # Organizer service initialize
#         organizer_service = OrganizerService(fs_service)
#         organizer_service.set_conversation_creator_method(
#             self.create_conversation)
#         organizer_service.add_source_can_load_method(
#             self.can_load_file_source)
#         organizer_service.add_source_can_load_method(
#             self.can_load_directory_source)
#         organizer_service.add_source_can_load_method(
#             self.can_load_transcribed_source)
#         profile_added = organizer_service.add_settings_profile_type(
#             self.DEFAULT_SETTINGS_TYPE, lambda data: GailBotSettings(data))
#         # pipeline initialize
#         pipeline = GBPipeline(pipeline_blackboard)
#         pipeline.configure_methods(
#             self.create_payload, self.create_metadata)
#         # Checking if fully configured
#         if configured and profile_added:
#             self.services = Services(
#                 fs_service, organizer_service, pipeline, True,
#                 BlackBoards(pipeline_blackboard, services_blackboard))
#         else:
#             self.services = Services()

#     ############################# MODIFIERS ###############################

#     def initialize(self) -> Services:
#         return self.services

#     ############################# PRIVATE METHODS ##########################

#     # -- Type 1: Checkers for organizer SourceLoader

#     def can_load_file_source(self, source_path: str) -> bool:
#         # Must be file.
#         if not self.io.is_file(source_path):
#             return False
#         # Must be supported.
#         _, source_extension = self.io.get_file_extension(source_path)
#         if not source_extension in self.io.get_supported_audio_formats() and \
#                 not source_extension in self.io.get_supported_video_formats():
#             return False
#         print("Loading source file")
#         return True

#     def can_load_directory_source(self, source_path: str) -> bool:
#         print("Loading source directory")
#         return self.io.is_directory(source_path)

#     def can_load_transcribed_source(self, source_path: str) -> bool:
#         if not self.io.is_directory(source_path):
#             return False
#         # Check if the metadata file exists
#         if not self._does_meta_exist(source_path):
#             return False
#         # Read the metatafile and use it to check other files
#         meta_path = self._get_meta_path(source_path)
#         did_read, meta_data = self.io.read(meta_path)
#         if meta_path == None or not did_read:
#             return False
#         try:
#             # The data should have been transcribed properly and
#             # raw files should be there.
#             print("Loading source transcribed")
#             return meta_data["is_transcribed"] and \
#                 self._check_raw_outputs(source_path, meta_data["outputs"])
#         except Exception as e:
#             return False

#     # -- Type 2: PipelineService methods

#     def create_payload(self, source) -> None:
#         print("Creating payload from source")
#         return Payload(source)

#     def create_metadata(self, conversation) -> Dict:
#         print("Creating metadata")

#     # -- Type 3: Conversation creator methods

#     def create_conversation(self, source_path: str) -> List[Dict]:
#         print("Creating conversation")
#         data_file_configs = list()
#         if self.io.is_file(source_path):
#             data_file_configs.append(
#                 self._create_data_file_config(source_path))
#         else:
#             supported_formats = list(self.io.get_supported_audio_formats())
#             supported_formats.extend(
#                 list(self.io.get_supported_video_formats()))
#             # NOTE: Check - adding additional gb_raw format to look for
#             supported_formats.append("gb")
#             _, file_paths = self.io.path_of_files_in_directory(
#                 source_path, supported_formats, False)
#             for path in file_paths:
#                 data_file_configs.append(
#                     self._create_data_file_config(path))
#         return data_file_configs

#     # Type 4: Helpers

#     def check_raw_outputs(
#             self, source_path,  output_paths: List[str]) -> bool:
#         raw_outputs = [path for path in output_paths if
#                        self.io.get_file_extension(path)
#                        == self.source_raw_transcription_extension]
#         # Ensure that this matches the actual raw files.
#         _, actual_paths = self.io.path_of_files_in_directory(
#             source_path, [self.source_raw_transcription_extension], False)
#         actual_names = [self.io.get_name(
#             path) for path in actual_paths]
#         for raw_output in raw_outputs:
#             if not self.io.get_name(raw_output) in actual_names:
#                 return False
#         return True

#     def _get_meta_path(self, source_path: str) -> str:
#         _, paths = self.io.path_of_files_in_directory(
#             source_path, [self.METADATA_EXTENSION], False)
#         return [path for path in paths if self.io.get_name(
#             path) == self.metadata_file_name][0]

#     def _does_meta_exist(self, source_path: str) -> bool:
#         _, paths = self.io.path_of_files_in_directory(
#             source_path, [self.METADATA_EXTENSION], False)
#         return len([path for path in paths if self.io.get_name(
#             path) == self.metadata_file_name]) > 0

#     def _create_data_file_config(self, source_file_path: str) -> Dict:
#         # configs = dict()
#         utterances = list()
#         if not self.io.is_file(source_file_path):
#             raise Exception()
#         if self.io.is_supported_audio_file(source_file_path):
#             file_type = "audio"
#         elif self.io.is_supported_video_file(source_file_path):
#             file_type = "video"
#         # -- NOTE: Check - assing handler for gb_raw file here!
#         elif self.io.get_file_extension(source_file_path)[1] == self.RAW_EXTENSION:
#             # Parse the raw file
#             # NOTE: The data file type needs to be changes / added maybe?
#             file_type = "audio"
#             data = open(source_file_path, "r").readlines()
#             for line in data:
#                 # NOTE: This split delimiter should also be in the
#                 # blackboard.
#                 tokens = line.split(",")
#                 utt = Utt(
#                     tokens[0],
#                     float(tokens[2]),
#                     float(tokens[3]),
#                     tokens[1])
#                 utterances.append(utt)
#         else:
#             raise Exception()
#         return {
#             "name": self.io.get_name(source_file_path),
#             "extension": self.io.get_file_extension(source_file_path)[1],
#             "file_type": file_type,
#             "path": source_file_path,
#             "size_bytes":  self.io.get_size(source_file_path)[1],
#             "utterances": utterances
#         }
