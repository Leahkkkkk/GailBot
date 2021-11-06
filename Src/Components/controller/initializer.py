from typing import Tuple, Dict, List, Any
from dataclasses import dataclass, asdict, fields
import json
import datetime

from Src.components.controller.pipeline.models import ProcessStatus

# Local imports
from ..io import IO
from ..config import Config
from ..services import FileSystemService, OrganizerService
from .configurables.gb_settings import GailBotSettings, GBSettingAttrs
from .pipeline import GBPipeline, Utt, Payload, ExternalMethods
from .configurables.blackboards import PipelineConfigLoader, PipelineBlackBoard,\
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


@dataclass
class MetaData:
    conversation_name: str
    settings_profile_name: str
    source_path: str
    conversation_source_type: str
    conversation_size: bytes
    transcription_date: datetime.date
    # TODO: the status returned is not a string. Fix this.
    # "transcription_status" : conversation.get_transcription_status(),
    transcription_time: datetime.time
    transcriber_name: str
    number_of_speakers: int
    number_of_source_files: int
    source_file_names: List[str]
    source_file_types: Dict[str, str]
    result_directory_path: str
    final_status: str
    plugins_applied: List[str]
    source_to_audio_map: Dict[str, str]


class GBInitializer:

    # TODO: THese should not be hard-coded here.
    DEFAULT_SETTINGS_TYPE = "gb"
    RAW_EXTENSION = "gb"
    METADATA_EXTENSION = "json"
    METADATA_NAME = "metadata"

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
            self.create_payload, self.create_metadata, self.stringify_utt,
            self.string_to_utt)
        pipeline = GBPipeline(
            blackboards.pipeline_blackboard, methods)
        return pipeline

    # ----------------------------- CONFIGURATION METHODS

    # -- Type 1: Checkers for organizer SourceLoader

    def can_load_file_source(self, source_path: str) -> bool:
        # Must be supported.
        _, source_extension = self.io.get_file_extension(source_path)
        return self.io.is_file(source_path) and \
            (source_extension in self.io.get_supported_audio_formats() or
             source_extension in self.io.get_supported_video_formats())

    def can_load_directory_source(self, source_path: str) -> bool:
        return self.io.is_directory(source_path)

    def can_load_transcribed_source(self, source_path: str) -> bool:
        # Has to be a directory with the metadata file
        if not self.io.is_directory(source_path):
            return False
        # The meta file must exist
        _, paths = self.io.path_of_files_in_directory(
            source_path, [self.METADATA_EXTENSION], False)
        if len([path for path in paths if self.io.get_name(
                path) == self.metadata_file_name]) == 0:
            return False
        meta_path = ([path for path in paths if self.io.get_name(
            path) == self.metadata_file_name])[0]
        # Read the metadata file
        did_read, meta_data = self.io.read(meta_path)
        if not did_read:
            return False
        # Verify the metadata file.
        # Dictionary should have all the keys in the MetaData object
        keys = [field.name for field in fields(MetaData)]
        if not all([k in meta_data.keys() for k in keys]):
            return False
        # Create metadata object
        meta_data = MetaData(**meta_data)
        # TODO: Check the raw output files exist
        return True

    # -- Type 2: PipelineService methods

    def create_payload(self, source: Source) -> None:
        if self.can_load_transcribed_source(source.source_path):
            return Payload(source, ProcessStatus.TRANSCRIBED)
        return Payload(source)

    def create_metadata(self, payload: Payload) -> Dict:
        """
        Create the metadata dictionary
        """
        conversation: Conversation = payload.source.conversation
        return asdict(MetaData(
            conversation.get_conversation_name(),
            payload.source.settings_profile_name,
            conversation.get_source_path(),
            conversation.get_source_type(),
            conversation.get_conversation_size(),
            conversation.get_transcription_date(),
            # TODO: the status returned is not a string. Fix this.
            # "transcription_status" : conversation.get_transcription_status(),
            conversation.get_transcription_time(),
            conversation.get_transcriber_name(),
            conversation.number_of_speakers(),
            conversation.number_of_source_files(),
            conversation.get_source_file_names(),
            conversation.get_source_file_types(),
            conversation.get_result_directory_path(),
            str(payload.status),
            list(payload.addons.plugin_summaires.keys()),
            json.dumps(payload.addons.source_to_audio_map)))

    # -- Type 3: Conversation creator methods

    def create_conversation(self, source_path: str) -> List[Dict]:
        data_file_configs = list()
        if self.io.is_file(source_path):
            data_file_configs.append(
                self.create_data_file_config(source_path))
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
                    self.create_data_file_config(path))
        return data_file_configs

    # --------- Type 4: Helpers

    def stringify_utt(self, utt: Utt) -> str:
        return "{}, {}, {}, {}".format(
            utt.speaker_label,
            utt.text,
            utt.start_time_seconds,
            utt.end_time_seconds)

    def string_to_utt(self, string: str) -> Utt:
        tokens = string.split(",")
        return Utt(
            tokens[0],
            float(tokens[2]),
            float(tokens[3]),
            tokens[1])

    def create_data_file_config(self, source_file_path: str) -> Dict:
        utterances = list()
        if not self.io.is_file(source_file_path):
            raise Exception()
        if self.io.is_supported_audio_file(source_file_path):
            file_type = "audio"
        elif self.io.is_supported_video_file(source_file_path):
            file_type = "video"
        elif self.io.get_file_extension(source_file_path)[1] \
                == self.RAW_EXTENSION:
            file_type = "audio"
            data = open(source_file_path, "r").readlines()
            utterances = [self.string_to_utt(s) for s in data]
        else:
            raise Exception()
        return {
            "name": self.io.get_name(source_file_path),
            "extension": self.io.get_file_extension(source_file_path)[1],
            "file_type": file_type,
            "path": source_file_path,
            "size_bytes":  self.io.get_size(source_file_path)[1],
            "utterances": utterances}
