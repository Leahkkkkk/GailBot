# Standard library imports
from typing import List, Dict, Any
# Local imports
from .services import ConfigService, OrganizerService, SourceDetails, \
                TranscriptionPipelineService, TranscriptionSummary, \
                GBSettingAttrs, SettingDetails
from .decorators import GBDecorators
from ..config import SystemBBAttributes
from ..organizer import Conversation
# Third party imports

class GailBotController:

    def __init__(self) -> None:
        ## Variables
        self.config_file_path = None
        self.previous_transcription_summary = None
        # TODO: These should be somewhere else
        self.default_transcriber_name = "GailBot"
        self.default_settings_profile_name = "default"
        ## Service objects
        self.config_service = ConfigService()
        self.organizer_service = OrganizerService()
        self.pipeline_service = TranscriptionPipelineService()

    ############################### MODIFIERS ################################

    ## OrganizerService

    @GBDecorators.check_configured
    def add_source(self, source_name : str, source_path : str,
            result_dir_path : str) -> bool:
        return self.organizer_service.add_source(
            source_name, source_path, result_dir_path,
            self.default_transcriber_name,self.default_settings_profile_name)

    @GBDecorators.check_configured
    def remove_source(self, source_name : str) -> bool:
        return self.organizer_service.remove_source(source_name)

    @GBDecorators.check_configured
    def clear_sources(self) -> bool:
        return self.organizer_service.clear_sources()

    @GBDecorators.check_configured
    def apply_settings_profile_to_source(self, source_name : str,
            settings_profile_name : str) -> bool:
        return self.organizer_service.apply_settings_profile_to_source(
            source_name,settings_profile_name)

    @GBDecorators.check_configured
    def save_custom_settings_profile(self, settings_profile_name : str) -> bool:
        return self.organizer_service.save_custom_settings_profile(
            settings_profile_name)

    @GBDecorators.check_configured
    def delete_custom_settings_profile(self, settings_profile_name : str) -> bool:
        return self.organizer_service.delete_custom_settings_profile(
            settings_profile_name)

    @GBDecorators.check_configured
    def create_new_custom_settings_profile(self, source_name : str,
            new_settings_profile_name : str) -> bool:
        return self.organizer_service.save_source_settings_profile(
            source_name,new_settings_profile_name)

    ## PipelineService

    @GBDecorators.check_configured
    def transcribe_all_sources(self) -> TranscriptionSummary:
        return self._transcribe_conversations(
            self.organizer_service.get_all_source_conversations().values())

    @GBDecorators.check_configured
    def transcribe_filtered_sources(self, source_names : List[str]) \
            -> TranscriptionSummary:
        return self._transcribe_conversations(
            self.organizer_service.get_filtered_source_conversations(
                source_names).values())

    ############################### GETTERS ##################################

    ## Controller
    def is_configured(self) -> bool:
        return self.config_service.is_fully_configured() and \
            self.organizer_service.is_configured() and \
            self.pipeline_service.is_configured()

    ## ConfigService

    @GBDecorators.check_configured
    def get_configuration_file_path(self) -> str:
        return self.config_service.get_configuration_file_path()

    ## OrganizerService

    @GBDecorators.check_configured
    def is_source(self, source_name : str) -> bool:
        return self.organizer_service.is_source(source_name)

    @GBDecorators.check_configured
    def get_source_names(self) -> List[str]:
        return self.organizer_service.get_source_names()

    @GBDecorators.check_configured
    def get_source_path(self) -> Dict[str,str]:
        return self.organizer_service.get_source_paths()

    @GBDecorators.check_configured
    def get_source_details(self, source_name : str) -> SourceDetails:
        return self.organizer_service.get_source_details()

    @GBDecorators.check_configured
    def get_filtered_source_details(self, source_names : List[str]) \
            -> Dict[str,SourceDetails]:
        return self.organizer_service.get_filtered_source_details(
            source_names)

    @GBDecorators.check_configured
    def get_all_source_details(self) -> Dict[str,SourceDetails]:
        return self.organizer_service.get_all_source_details()

    @GBDecorators.check_configured
    def is_settings_profile(self, settings_profile_name : str) -> bool:
        return self.organizer_service.is_settings_profile(settings_profile_name)

    @GBDecorators.check_configured
    def get_source_settings_profile_name(self, source_name : str) -> str:
        return self.organizer_service.get_source_settings_profile_name(
            source_name)

    @GBDecorators.check_configured
    def get_all_settings_profiles_names(self) -> List[str]:
        return self.organizer_service.get_settings_profile_names()

    @GBDecorators.check_configured
    def get_source_settings_profile_details(self, source_name : str) \
            -> SettingDetails:
        return self.organizer_service.get_source_settings_profile_details(
            source_name)

    @GBDecorators.check_configured
    def get_all_settings_profiles_details(self) -> Dict[str,SettingDetails]:
        return self.get_all_settings_profiles_details()

    ################################ SETTERS #################################

    ## Controller

    @GBDecorators.check_configured
    def set_settings_profile_attribute(self, settings_profile_name : str,
            attribute : GBSettingAttrs, value : Any) -> bool:
        pass

    @GBDecorators.check_configured
    def set_source_settings_profile_attribute(self, source_name : str,
            attribute : GBSettingAttrs, value : Any) -> bool:
        pass

    ## ConfigService

    def set_configuration_file_path(self, path : str) -> bool:
        return self.config_service.set_configuration_file_path(path) and \
            self.config_service.configure_from_path() and \
            self._initialize_services()

    ############################ PRIVATE METHODS #############################

    ## Services

    def _initialize_services(self) -> bool:
        return self._configure_config_service() and \
            self._configure_organizer_service() and \
            self._configure_pipeline_service()

    def _configure_config_service(self) -> bool:
        return self.config_service.is_fully_configured()

    def _configure_organizer_service(self) -> bool:
        if not self.config_service.is_fully_configured():
            return False
        system_bb = self.config_service.get_system_blackboard()
        ws_path = system_bb.get(SystemBBAttributes.default_workspace_path)[1]
        self.organizer_service.set_workspace_path(ws_path)
        return self.organizer_service.is_configured()

    def _configure_pipeline_service(self) -> bool:
        return self.pipeline_service.is_configured()

    ## PipelineService

    def _transcribe_conversations(self, conversations : List[Conversation]) \
            -> TranscriptionSummary:
        self.pipeline_service.clear_conversations()
        self.pipeline_service.add_conversations_to_transcribe(
            conversations)
        self.pipeline_service.start_transcription_process()
        return self.pipeline_service.get_transcription_summary()




