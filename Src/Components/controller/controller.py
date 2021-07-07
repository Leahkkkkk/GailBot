# Standard library imports
from typing import List, Dict, Any, Tuple
# Local imports
from .services import FileSystemService, ConfigService,OrganizerService, \
    SettingsDetails,SourceDetails,PipelineServiceSummary,PipelineService, \
    GBSettingAttrs

class GailBotController:

    def __init__(self, workspace_dir_path : str) -> None:
        ## Vars.
        self.pipeline_service_num_threads = 3
        ## Objects
        self.fs_service = FileSystemService()
        if not self.fs_service.configure_from_workspace_path(workspace_dir_path):
            raise Exception("FileSystemService not configured")
        self.config_service = ConfigService(self.fs_service)
        if not self.config_service.is_configured():
            raise Exception("ConfigService not configured")
        self.organizer_service = OrganizerService(self.fs_service)
        self.pipeline_service = PipelineService(
            self.pipeline_service_num_threads)

    ############################### MODIFIERS ################################

    def shutdown(self) -> None:
        self.fs_service.shutdown()

    def add_source(self, source_name : str, source_path : str,
            result_dir_path : str, transcriber_name : str = "GailBot"):
        return self.organizer_service.add_source(
            source_name, source_path, result_dir_path, transcriber_name)

    def remove_source(self, source_name : str) -> bool:
        return self.organizer_service.remove_source(source_name)

    def remove_sources(self, source_names : List[str]) -> bool:
        return self.organizer_service.remove_sources(source_names)

    def clear_sources(self) -> bool:
        return self.organizer_service.clear_sources()

    def reset_source(self, source_name : str) -> bool:
        return self.organizer_service.reset_source(source_name)

    def reset_sources(self, source_names : List[str]) -> bool:
        return self.organizer_service.reset_sources(source_names)

    def reset_all_sources(self) -> bool:
        return self.organizer_service.reset_all_sources()

    def create_new_settings_profile(
        self, new_settings_profile_name : str, data : Dict[GBSettingAttrs,Any]) \
                -> bool:
        return self.organizer_service.create_new_settings_profile(
            new_settings_profile_name,data)

    def save_settings_profile(self, settings_profile_name : str) -> bool:
        return self.organizer_service.save_settings_profile(
            settings_profile_name)

    def remove_settings_profile(self, settings_profile_name : str) -> bool:
        return self.organizer_service.remove_settings_profile(
            settings_profile_name)

    def remove_all_settings_profiles(self) -> bool:
        return self.organizer_service.remove_all_settings_profiles()

    def change_settings_profile_name(self, settings_profile_name : str,
            new_name : str) -> bool:
        return self.organizer_service.change_settings_profile_name(
            settings_profile_name, new_name)

    def apply_settings_profile_to_source(self, source_name : str,
            settings_profile_name : str) -> bool:
        return self.organizer_service.apply_settings_profile_to_source(
            source_name, settings_profile_name)

    def apply_settings_profile_to_sources(self, source_names : List[str],
            settings_profile_name : str) -> bool:
        return self.organizer_service.apply_settings_profile_to_sources(
            source_names, settings_profile_name)

    def save_source_settings_profile(self, source_name : str,
            new_settings_profile_name : str)  -> bool:
        return self.organizer_service.save_source_settings_profile(
            source_name, new_settings_profile_name)

    def register_analysis_plugins(self, config_path : str) -> List[str]:
        return self.pipeline_service.register_analysis_plugins(config_path)

    def register_format(self, config_path : str) -> Tuple[str,List[str]]:
        return self.pipeline_service.register_format(config_path)

    def transcribe(self) -> PipelineServiceSummary:
        sources = self.organizer_service.get_configured_sources()
        self.pipeline_service.add_sources(sources)
        return self.pipeline_service.start()

     ############################## GETTERS ###################################

    def get_supported_audio_formats(self) -> List[str]:
        return self.organizer_service.get_supported_audio_formats()

    def get_supported_video_formats(self) -> List[str]:
        return self.organizer_service.get_supported_audio_formats()

    def is_source(self, source_name : str) -> bool:
        return self.organizer_service.is_source(source_name)

    def is_source_ready_to_transcribe(self, source_name : str) -> bool:
        return self.organizer_service.is_source_configured(source_name)

    def get_source_names(self) -> List[str]:
        return self.organizer_service.get_source_names()

    def get_names_of_sources_ready_to_transcribe(self) -> List[str]:
        return self.organizer_service.get_configured_source_names()

    def get_source_details(self, source_name : str) -> SourceDetails:
        return self.organizer_service.get_source_details(source_name)

    def get_sources_details(self, source_names : List[str]) \
            -> Dict[str,SourceDetails]:
        return self.organizer_service.get_sources_details(source_names)

    def get_all_source_details(self) -> Dict[str,SourceDetails]:
        return self.organizer_service.get_all_source_details()

    def is_settings_profile(self, settings_profile_name : str) -> bool:
        return self.organizer_service.is_settings_profile(settings_profile_name)

    def is_settings_profile_saved(self, settings_profile_name : str) -> bool:
        return self.organizer_service.is_settings_profile_saved(
            settings_profile_name)

    def get_settings_profile_details(self, settings_profile_name : str) \
            -> SettingsDetails:
        return self.organizer_service.get_settings_profile_details(
            settings_profile_name)

    def get_settings_profiles_details(self,
            settings_profile_names : List[str]) -> Dict[str,SettingsDetails]:
        return self.organizer_service.get_settings_profiles_details(
            settings_profile_names)

    def get_all_settings_profiles_details(self) -> Dict[str,SettingsDetails]:
        return self.organizer_service.get_all_settings_profiles_details()

    def get_source_settings_profile_name(self, source_name) -> str:
        return self.organizer_service.get_source_settings_profile_name(
            source_name)

    def get_source_names_using_settings_profile(self,
            settings_profile_name : str) -> List[str]:
        return self.organizer_service.get_source_names_using_settings_profile(
            settings_profile_name)

    def get_sources_details_using_settings_profile(self,
            settings_profile_name : str) -> Dict[str,SourceDetails]:
        return self.organizer_service.get_sources_details_using_settings_profile(
            settings_profile_name)

    def get_source_settings_profile_details(self, source_name : str) \
            -> SettingsDetails:
        return self.organizer_service.get_source_settings_profile_details(
            source_name)

    def get_sources_settings_profile_details(self, source_names : List[str]) \
            -> Dict[str,SettingsDetails]:
        return self.organizer_service.get_sources_settings_profile_details(
            source_names)

    def get_all_sources_settings_profile_details(self) \
            -> Dict[str,SettingsDetails]:
        return self.organizer_service.get_all_sources_settings_profile_details()

    def get_analysis_plugin_names(self) -> List[str]:
        return self.pipeline_service.get_analysis_plugin_names()

    def get_format_names(self) -> List[str]:
        return self.pipeline_service.get_format_names()

    def get_format_plugin_names(self, format_name  : str) -> List[str]:
        return self.pipeline_service.get_format_plugin_names(format_name)

    ############################## SETTERS ###################################

    def set_settings_profile_attribute(self,settings_profile_name : str,
            attr : GBSettingAttrs, value : Any) -> bool:
        return self.organizer_service.set_settings_profile_attribute(
            settings_profile_name,attr, value)

    def set_source_settings_profile_attribute(self, source_name : str,
            attr : GBSettingAttrs, value : Any) -> bool:
        return self.organizer_service.set_source_settings_profile_attribute(
            source_name, attr, value)


