# Standard library imports
from Src.Components.config.attributes import SystemBBAttributes
from Src.Components.controller.services.organizer_service.setting_details import SettingDetails
from Src.Components.organizer.conversation import Conversation
from typing import List, Dict, Any
# Local imports
from .services import ConfigService, OrganizerService, SourceDetails, \
                TranscriptionPipelineService, TranscriptionSummary
from ..organizer import Settings
# Third party imports


class GailBotController:

    def __init__(self, configuration_file_path : str) -> None:
        # Variables
        self.configuration_file_path = configuration_file_path
        self.previous_transcription_summary = None
        # Service objects
        self.config_service = ConfigService()
        self.organizer_service = OrganizerService()
        self.pipeline_service = TranscriptionPipelineService()
        ### Initialize all service objects
        if not self._initialize_config_service(self.configuration_file_path):
             raise Exception("Configuration service could not be initialized")
        # Obtain relevant blackboards tp configure other services.
        system_blackboard = self.config_service.get_system_blackboard()
        ws_path = system_blackboard.get(
            SystemBBAttributes.default_workspace_path)[1]
        if not self._initialize_organizer_service(ws_path , "{}/{}".format(
                ws_path,"conversation_ws")):
            raise Exception("Organizer service could not be initialized")
        if not self._initialize_pipeline_service():
            raise Exception("Pipeline service could not be initialized")

    ############################### MODIFIERS ################################

    ### Controller

    # def reset_controller(self) -> bool:
    #     pass

    ### Source

    def add_source(self, source_name : str, source_path : str,
            result_dir_path : str) -> bool:
        if not self._is_controller_configured():
            return False
        return self.organizer_service.add_source(
            source_name, source_path, result_dir_path,"GailBot")

    def remove_source(self, source_name : str) -> bool:
        if not self._is_controller_configured():
            return False
        return self.organizer_service.remove_source(source_name)

    def remove_sources(self, source_names : List[str]) -> bool:
        if not self._is_controller_configured():
            return False
            return False
        for source_name in source_names:
            if not self.organizer_service.remove_source(source_name):
                return False
        return True

    def remove_all_sources(self) -> bool:
        if not self._is_controller_configured():
            return False
        return self.organizer_service.clear_sources()

    ### Transcription

    def transcribe_all_sources(self) -> TranscriptionSummary:
        if not self.is_ready_to_transcribe():
            return False
        self.pipeline_service.clear_conversations()
        self.pipeline_service.add_conversations_to_transcribe(
            self.organizer_service.get_all_sources_conversations())
        summary =  self.pipeline_service.get_transcription_summary()
        self.previous_transcription_summary = summary
        return summary

    def transcribe_filtered_sources(self, source_names : List[str]) \
            -> TranscriptionSummary:
        if not self.is_ready_to_transcribe():
            return False
        conversations = [self.organizer_service.get_source_conversation(
            source_name) for source_name in source_names]
        self.pipeline_service.clear_conversations()
        self.pipeline_service.add_conversations_to_transcribe(conversations)
        summary =  self.pipeline_service.get_transcription_summary()
        self.previous_transcription_summary = summary
        return summary

    ### Settings profiles

    def save_source_settings_profile(self, source_name : str) -> bool:
        if not self._is_controller_configured():
            return False
        custom_profile_name = "{}_settings".format(source_name)
        return self.organizer_service.save_source_settings(
            source_name,custom_profile_name)

    def delete_source_settings_profile(self, source_name : str) -> bool:
        if not self._is_controller_configured():
            return False
        custom_profile_name = "{}_settings".format(source_name)
        return self.organizer_service.delete_setting(custom_profile_name)

    def delete_all_custom_settings_profiles(self) -> bool:
        if not self._is_controller_configured():
            return False
        setting_names = self.organizer_service.get_available_setting_names()
        for setting_name in setting_names:
            # TODO: This should be managed by organizer service i.e.,
            # default setting cannot be deleted.
            if setting_name != "default":
                if not self.delete_custom_settings_profile(setting_name):
                    return False
        return True

    def delete_custom_settings_profile(self, settings_profile_name : str) -> bool:
        if not self._is_controller_configured():
            return False
        return self.organizer_service.delete_setting(settings_profile_name)

    ############################### GETTERS ##################################

    ### Controller

    def is_ready_to_transcribe(self) -> bool:
        return self._is_controller_configured() and \
            len(self.organizer_service.get_source_names) > 0

    ### Source

    def is_source(self, source_name : str) -> bool:
        return self.organizer_service.is_source(source_name)

    def get_source_names(self) -> List[str]:
        return self.organizer_service.get_source_names()

    def get_source_paths(self) -> Dict[str,str]:
        return self.organizer_service.get_source_paths()

    def get_source_details(self, source_name : str) -> SourceDetails:
        return self.organizer_service.get_source_details(source_name)

    # TODO: Add a method in organizer service to refer to settings by name
    # And get the name of the settings of a source.
    def get_source_settings_profile_name(self, source_name : str) -> str:
        pass

    ### Transcription

    def get_previous_transcription_summary(self) -> TranscriptionSummary:
        return self.previous_transcription_summary

    ### Settings profile.

    def is_settings_profile(self, settings_profile_name : str) -> bool:
        return self.organizer_service.is_setting(settings_profile_name)

    # TODO: Add a method in organizer service to refer to setting_profiles by name.
    def get_settings_profile_details(self, settings_profile_name : str) -> SettingDetails:
        pass

    def get_all_settings_profile_names(self) -> List[str]:
        return self.organizer_service.get_available_setting_names()

    def get_all_settings_profile_details(self) -> Dict[str,SettingDetails]:
        return self.organizer_service.get_available_setting_details()

    ################################ SETTERS #################################

    ### Controller

    ### Source

    # TODO: Add method in organizer service to do this.
    def set_source_settings_profile(self, source_name : str,
            settings_profile_name : str) -> bool:
        pass

    ### Transcription

    ### Settings profile

    # TODO: Determine mechanism to do this.
    def set_settings_profile_attribute(self, settings_profile_name : str,
            attribute : Any, value : Any) -> bool:
        pass


    ############################ PRIVATE METHODS #############################

    def _initialize_config_service(self, configuration_file_path : str) -> bool:
        self.config_service.set_configuration_file_path(configuration_file_path)
        return self.config_service.is_fully_configured()

    def _initialize_organizer_service(self,workspace_path : str,
            conversation_workspace_path : str) -> bool:
        self.organizer_service.set_workspace_path(workspace_path)
        self.organizer_service.set_conversation_workspace_path(
            conversation_workspace_path)
        return self.organizer_service.is_fully_configured()

    def _initialize_pipeline_service(self) -> bool:
        return self.pipeline_service.is_fully_configured()

    def _are_services_initialized(self) -> bool:
        return self.config_service.is_fully_configured() and \
            self.organizer_service.is_fully_configured() and \
            self.pipeline_service.is_fully_configured()

    def _is_controller_configured(self) -> bool:
        return self._are_services_initialized()
