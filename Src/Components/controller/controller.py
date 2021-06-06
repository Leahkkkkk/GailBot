
# Standard library imports
from typing import List, Any, Dict
# Local imports
from .services import FileSystemService,ConfigService,OrganizerService,\
                TranscriptionPipelineService, GBSettingAttrs, TranscriptionSummary,\
                SettingDetails, SourceDetails
from ..organizer import Conversation
# Third party imports


class GailBotController:

    def __init__(self, workspace_dir_path : str) -> None:
        ## Objects
        self.fs_service = FileSystemService()
        self.fs_service.configure_from_workspace_path(workspace_dir_path)
        if not self.fs_service.is_configured():
            raise Exception("FileSystemService not configured")
        self.config_service = ConfigService(self.fs_service)
        self.organizer_service = OrganizerService(self.fs_service)
        self.pipeline_service = TranscriptionPipelineService()
        # Initializing all services
        self._initialize_config_service(self.config_service)
        self._initialize_organizer_service(self.organizer_service)
        self._initialize_pipeline_service(self.pipeline_service)

    ############################### MODIFIERS ################################

    ## OrganizerService

    # TODO: Needs more checks for invalid inputs
    def add_source(self, source_name : str, source_path : str,
            result_dir_path : str, transcriber_name : str = "GailBot"):
        """
        Add a source to be transcribed.
        """
        return self.organizer_service.add_source(
            source_name, source_path, result_dir_path,transcriber_name)

    def remove_source(self, source_name : str) -> bool:
        """
        Remove a single source.
        """
        return self.organizer_service.remove_source(source_name)

    def remove_sources(self, source_names : List[str]) -> bool:
        """
        Remove multiple sources.
        """
        return self.organizer_service.remove_sources(source_names)

    def clear_sources(self) -> bool:
        """
        Remove all sources.
        """
        return self.organizer_service.clear_sources()

    def reset_source(self, source_name : str) -> bool:
        """
        Reload the specified source.
        """
        return self.organizer_service.reset_source(source_name)

    def reset_sources(self, source_names : List[str]) -> bool:
        """
        Reload the specified sources.
        """
        return self.organizer_service.reset_sources(source_names)

    def reset_all_sources(self) -> bool:
        """
        Reload all sources.
        """
        return self.organizer_service.reset_all_sources()

    def create_new_settings_profile(self, new_settings_profile_name : str,
            data : Dict[GBSettingAttrs,Any]) -> bool:
        """
        Create a new settings profile from the given data.
        """
        return self.organizer_service.create_new_settings_profile(
            new_settings_profile_name, data)

    def save_settings_profile(self, settings_profile_name : str) -> bool:
        """
        Save the given settings profile to disk.
        """
        return self.organizer_service.save_settings_profile(
            settings_profile_name)

    def remove_settings_profile(self, settings_profile_name : str) -> bool:
        """
        Remove the given settings profile from both memory and disk.
        """
        return self.organizer_service.remove_settings_profile(
            settings_profile_name)

    def remove_all_settings_profiles(self) -> bool:
        """
        Remove all the settings profiles from both memory and disk.
        """
        return self.organizer_service.remove_all_settings_profiles()

    def change_settings_profile_name(self, settings_profile_name : str,
            new_profile_name : str) -> bool:
        """
        Change the name of an existing settings profile both in memory and disk.
        """
        return self.organizer_service.change_settings_profile_name(
            settings_profile_name, new_profile_name)

    def apply_settings_profile_to_source(self, source_name : str,
            settings_profile_name : str) -> bool:
        """
        Apply the specified settings profile to the specified source.
        """
        return self.organizer_service.apply_settings_profile_to_source(
            source_name, settings_profile_name)

    def save_source_settings_profile(self, source_name : str,
            new_settings_profile_name : str) -> bool:
        """
        Save the specified source's settings profile to disk with the defined
        name.
        """
        return self.organizer_service.save_source_settings_profile(
            source_name, new_settings_profile_name)

    ## PipelineService

    def transcribe_all_sources(self) -> TranscriptionSummary:
        """
        Transcribe all configured sources and obtain a transcription summary
        """
        conversations = list(self.organizer_service.\
            get_all_configured_source_conversations().values())
        return self._start_transcription_pipeline(conversations)

    def transcribe_sources(self, source_names : List[str]) \
            -> TranscriptionSummary:
        """
        Transcribe the given sources if they are configured.
        """
        conversations = list(self.organizer_service.\
            get_configured_sources_conversations(source_names).values())
        return self._start_transcription_pipeline(conversations)

    def transcribe_source(self, source_name : str) -> TranscriptionSummary:
        """
        Transcribe the given source.
        """
        if not self.is_source_ready_to_transcribe(source_name):
            return
        conversation =\
            self.organizer_service.get_configured_source_conversation(
                source_name)
        return self._start_transcription_pipeline([conversation])
    ############################### GETTERS ##################################

    ## OrganizerService

    def is_source(self, source_name : str) -> bool:
        """
        Determine if the given source exists.
        """
        return self.organizer_service.is_source(source_name)

    def is_source_ready_to_transcribe(self, source_name : str) -> bool:
        """
        Determine if the given source is ready to transcribe.
        """
        return self.organizer_service.is_source_configured(source_name)

    def get_source_names(self) -> List[str]:
        """
        Obtain the names of all sources.
        """
        return self.organizer_service.get_source_names()

    def get_names_of_sources_ready_to_transcribe(self) -> List[str]:
        """
        Obtain the names of all sources that are ready to transcribe.
        """
        return self.organizer_service.get_configured_source_names()

    def get_source_details(self, source_name : str) -> SourceDetails:
        """
        Obtain details for the specified source.
        """
        return self.organizer_service.get_source_details(source_name)

    def get_all_source_details(self) -> Dict[str,SourceDetails]:
        """
        Obtain the details for all sources.
        """
        return self.organizer_service.get_all_source_details()

    def is_settings_profile(self, settings_profile_name : str) -> bool:
        """
        Determine if the given settings profile exists.
        """
        return self.organizer_service.is_settings_profile(settings_profile_name)

    def is_settings_profile_saved(self, settings_profile_name : str) -> bool:
        """
        Determine if the given settings profile is saved on disk.
        """
        return self.organizer_service.is_settings_profile_saved(
            settings_profile_name)

    def get_settings_profile_details(self, settings_profile_name : str) \
            -> SettingDetails:
        """
        Obtain the details of the specified details.
        """
        return self.organizer_service.get_settings_profile_details(
            settings_profile_name)

    def get_all_settings_profile_details(self) -> Dict[str,SettingDetails]:
        """
        Obtain the details of all settings profiles.
        """
        return self.organizer_service.get_all_settings_profiles_details()

    def get_source_settings_profile_name(self, source_name : str) -> str:
        """
        Get the settings profile associated with the given settings profile.
        """
        return self.organizer_service.get_source_settings_profile_name(
            source_name)

    def get_source_names_using_settings_profile(self,
            settings_profile_name : str) -> List[str]:
        """
        Obtain the names of all the sources using the specified settings profile.
        """
        return self.organizer_service.get_source_names_using_settings_profile(
            settings_profile_name)

    def get_sources_details_using_settings_profile(self,
            settings_profile_name : str) -> Dict[str,SourceDetails]:
        """
        Obtain the details of all the sources using the specified settings
        details.
        """
        return self.organizer_service.get_sources_details_using_settings_profile(
            settings_profile_name)

    def get_source_settings_profile_details(self, source_name : str) \
            -> SettingDetails:
        """
        Get source settings profile details.
        """
        return self.organizer_service.get_source_settings_profile_details(
            source_name)

    def get_sources_settings_profile_details(self, source_names : List[str]) \
            -> Dict[str,SettingDetails]:
        """
        Get the settings profile details for the specified sources.
        """
        return self.organizer_service.get_sources_settings_profile_details(
            source_names)

    def get_all_sources_settings_profile_details(self) \
            -> Dict[str,SettingDetails]:
        """
        Get the settings profile details of all sources.
        """
        return self.organizer_service.get_all_sources_settings_profile_details()

    # TODO: This needs to be implemented in a service.
    def get_supported_audio_formats(self) -> List[str]:
        pass

    # TODO: This needs to be implemented in a service.
    def get_supported_video_formats(self) -> List[str]:
        pass


    ################################ SETTERS #################################

    ## OrganizerService

    def set_settings_profile_attribute(self,settings_profile_name : str,
            attr : GBSettingAttrs, value : Any) -> bool:
        """
        Set the settings profile attribute for the specified profile both in
        memory and on disk.
        """
        return self.organizer_service.set_source_settings_profile_attribute(
            settings_profile_name,attr,value)

    def set_source_settings_profile_attribute(self, source_name : str,
            attr : GBSettingAttrs, value : Any) -> bool:
        """
        Set the settings profile attribute for the specified source only.
        """
        return self.organizer_service.set_source_settings_profile_attribute(
            source_name, attr, value)

    ############################ PRIVATE METHODS #############################

    def _initialize_config_service(self, service : ConfigService) -> None:
        if not service.configure_from_path():
            raise Exception("ConfigService not configured")

    def _initialize_organizer_service(self, service : OrganizerService) \
            -> None:
        if not service.is_configured():
            raise Exception("OrganizerService not configured")

    def _initialize_pipeline_service(self,
            service : TranscriptionPipelineService) -> None:
        pass

    def _start_transcription_pipeline(self, conversations : List[Conversation])\
            -> TranscriptionSummary:
        self.pipeline_service.add_conversations(conversations)
        return self.pipeline_service.start_transcription_pipeline()

