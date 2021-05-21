# Standard library imports
from typing import List, Dict, Any
# Local imports
from .services import ConfigService, OrganizerService, SourceDetails, \
                TranscriptionPipelineService, TranscriptionSummary
from ..organizer import Settings
# Third party imports

class GailBotController:

    def __init__(self) -> None:
        # Service Objects
        self.organizer_service = OrganizerService()
        self.config_service = ConfigService()
        self.transcription_pipeline = TranscriptionPipelineService()


    ############################### MODIFIERS ################################

    def add_source(self, source_name : str, source_path : str) -> bool:
        pass

    def remove_source(self, source_name : str) -> bool:
        pass

    def clear_sources(self) -> bool:
        pass

    def apply_settings_to_source(self, source_name : str, settings : Settings) -> bool:
        pass

    def transcribe_all_sources(self) -> bool:
        pass

    def transcribe_filtered_sources(self, source_names : List[str]) -> bool:
        pass

    def initialize_setting_of_type(self, settings_name : str) -> Settings:
        pass

    ############################### SETTERS ##################################

    ## Controller
    def set_configuration_file_path(self, config_file_path : str) -> bool:
        pass

    ## Source
    def set_source_transcriber_name(self, source_name : str, transcriber_name : str) -> bool:
        pass

    ################################ GETTERS #################################
    ## Controller

    def is_ready_to_transcribe(self) -> bool:
        pass

    def get_transcription_summary(self) -> TranscriptionSummary:
        pass

    def get_configuration_file_path(self) -> str:
        pass

    ## Source

    def is_source(self, source_name : str) -> bool:
        pass

    # TODO: Change the return type to a SourceDetails object.
    def get_source_details(self, source_name : str) -> SourceDetails:
        pass

    def get_source_names(self) -> List[str]:
        pass

    def get_source_paths(self) -> List[str]:
        pass

    ## Settings

    def get_supported_setting_types(self) -> List[str]:
        pass

    ############################ PRIVATE METHODS #############################

    def _is_configured(self) -> bool:
        pass

    def _is_pipeline_ready(self) -> bool:
        pass





