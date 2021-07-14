from dataclasses import dataclass
from typing import Dict, Any
# Local imports
from ......utils.logger import BaseLogHandler
from .....organizer import Conversation
from ...fs_service import SourceHook
from .source_logs import ErrorLogHandler, ConsoleLogHandler, FileLogHandler, \
        RequestType
from .hook_observer import SourceHookObserver


class Source:

    def __init__(self, source_name : str, source_path : str,
            transcriber_name : str, hook : SourceHook) -> None:
        self.source_name : str = source_name
        self.source_path : str = source_path
        self.transcriber_name : str = transcriber_name
        self.settings_profile_name : str = None
        self.conversation : Conversation = None
        self.configured : bool = False
        self.hook : SourceHook = hook
        # Initializing logger
        self.logger = self._initialize_logger(hook)
        # Adding observer to hook
        self.source_hook_observer = SourceHookObserver(self.logger)
        self.hook.register_listener("add_to_source",self.source_hook_observer)
        self.hook.register_listener("remove_from_source",self.source_hook_observer)
        self.hook.register_listener("cleanup",self.source_hook_observer)
        self.hook.register_listener("save_to_directory",self.source_hook_observer)

    def __del__(self) -> None:
        self.log(RequestType.FILE,"source deleted")

    ################################## MODIFIERS ############################

    def log(self, event_type : RequestType, request : str) -> None:
        self.logger.handle(event_type,request)

    ################################## GETTERS ##############################

    def get_source_name(self) -> str:
        return self.source_name

    def get_source_path(self) -> str:
        return self.source_path

    def get_result_directory_path(self) -> str:
        return self.hook.get_result_directory_path()

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

    ################################## SETTERS #############################

    def set_transcriber_name(self, transcriber_name : str) -> None:
        self.transcriber_name = transcriber_name

    def set_settings_profile_name(self, settings_profile_name : str) -> None:
        self.settings_profile_name = settings_profile_name

    def set_conversation(self, conversation : Conversation) -> None:
        self.conversation = conversation

    def set_configured(self) -> None:
        self.configured = True

    ################################ PRIVATE METHODS ########################

    def _initialize_logger(self, hook : SourceHook) -> BaseLogHandler:
        file_logger = FileLogHandler(hook.get_result_directory_path())
        error_logger = ErrorLogHandler(hook.get_result_directory_path())
        console_logger = ConsoleLogHandler()
        error_logger.set_next(console_logger)
        file_logger.set_next(error_logger)
        return file_logger

