from dataclasses import dataclass
# Local imports
from ...organizer import Conversation
from .fs_service import SourceHook
from....utils.logger import BaseLogHandler
from .source_logs import ErrorLogHandler, ConsoleLogHandler, FileLogHandler

class Source:

    def __init__(self) -> None:
        self.source_name : str = None
        self.source_path : str = None
        self.result_dir_path : str = None
        self.transcriber_name : str = None
        self.settings_profile_name : str = None
        self.conversation : Conversation = None
        self.configured : bool = False
        self.hook : SourceHook = None
        self.logger = self._initialize_logger()

    ################################## GETTERS ##############################

    def get_source_name(self) -> str:
        return self.source_name

    def get_source_path(self) -> str:
        return self.source_path

    def get_result_directory_path(self) -> str:
        return self.result_dir_path

    def get_transcriber_name(self) -> str:
        return self.transcriber_name

    def get_settings_profile_name(self) -> str:
        return self.settings_profile_name

    def get_conversation(self) -> Conversation:
        return self.conversation

    def is_configured(self) -> bool:
        return self.configured

    def get_hook(self) -> SourceHook:
        return self.hook

    def get_logger(self) -> BaseLogHandler:
        return self.logger

    ################################## SETTERS #############################

    def set_source_name(self, source_name : str) -> None:
        self.source_name = source_name

    def set_source_path(self, source_path : str) -> None:
        self.source_path = source_path

    def set_result_directory_path(self, dir_path : str) -> None:
        self.result_dir_path = dir_path

    def set_transcriber_name(self, transcriber_name : str) -> None:
        self.transcriber_name = transcriber_name

    def set_settings_profile_name(self, settings_profile_name : str) -> None:
        self.settings_profile_name = settings_profile_name

    def set_conversation(self, conversation : Conversation) -> None:
        self.conversation = conversation

    def set_hook(self, hook : SourceHook) -> None:
        self.hook = hook

    def set_configured(self) -> None:
        self.configured = True

    ################################ PRIVATE METHODS ########################

    def _initialize_logger(self) -> BaseLogHandler:
        return ErrorLogHandler().set_next(ConsoleLogHandler().set_next(
            FileLogHandler()))




