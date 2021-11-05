# Standard imports
from typing import List, Any, Dict
# Local imports
from .helpers.gb_settings import GBSettingAttrs, GailBotSettings
from .initializer import GBInitializer, Services
from .pipeline import GBPipeline
from ..services import FileSystemService, OrganizerService, SourceDetails, \
    SettingsDetails


class GailBotController:
    """
    Provides an API to use GailBot.
    """

    def __init__(self, workspace_dir_path: str) -> None:
        self.initializer = GBInitializer()
        self.services = self.initializer.initialize(workspace_dir_path)
        if not self.services.is_initialized:
            raise Exception("Controller cannot be initialized")
        self.fs_service = self.services.fs_service
        self.organizer_service = self.services.organizer_service
        self.pipeline = self.services.pipeline

    ############################### MODIFIERS ###############################

    def shutdown(self) -> None:
        """
        Shutdown the controller components properly.
        """
        self.fs_service.shutdown()

    def add_source(self, source_name: str, source_path: str,
                   result_dir_path: str, transcriber_name: str = "gb") -> bool:
        """
        Add a source.

        Args:
            source_name (str): Name of the source. Must be unique.
            source_path (str): Path to the source. Can be file or directory.
            result_dir_path (str): Path to the result directory.
            transcriber_name (str): Name of the transcriber for this source.

        Returns:
            (bool): True if added successfully. False otherwise.
        """
        return self.organizer_service.add_source(
            source_name, source_path, result_dir_path, transcriber_name)

    def remove_source(self, source_name: str) -> bool:
        """
        Remove a source that has been added.

        Args:
            source_name (str): Name of the source.

        Returns:
            (bool): True if removed successfully, False otherwise.
        """
        return self.organizer_service.remove_source(source_name)

    def remove_sources(self, source_names: List[str]) -> bool:
        """
        Remove multiple sources that have been previously added.

        Args:
            source_names (List[str]): Names of sources to remove.

        Returns:
            (bool): True if all sources have been removed, False otherwise.
        """
        return self.organizer_service.remove_sources(source_names)

    def clear_sources(self) -> bool:
        """
        Remove all sources.

        Returns:
            (bool): True if all sources are removed, False otherwise.
        """
        return self.organizer_service.clear_sources()

    def reset_source(self, source_name: str) -> bool:
        """
        Reset the specified source, removing any attached settings profiles.

        Args:
            source_name (str): Name of the source.

        Returns:
            (bool): True if successfully reset, False otherwise.
        """
        return self.organizer_service.reset_source(source_name)

    def reset_sources(self, source_names: List[str]) -> bool:
        """
        Reset all the specified sources, removing any attached settings profile.

        Args:
            source_names (List[str]): Names of sources to reset.
        """
        return self.organizer_service.reset_sources(source_names)

    def reset_all_sources(self) -> bool:
        """
        Reset all sources that are present.

        Returns:
            (bool): True if all sources are reset, False otherwise.
        """
        return self.organizer_service.reset_all_sources()

    def create_new_settings_profile(self, new_settings_profile_name: str,
                                    data: Dict[GBSettingAttrs, Any]) -> bool:
        """
        Create a new settings profiles with the specified data.
        Note that this profile is not automatically saved to disk.

        Args:
            new_settings_profile_name (str):
                Name of the new profile. Must be unique.
            data (Dict[GBSettingAttrs,Any]):
                Mapping from settings attribute to its value.

        Returns:
            (bool): True if profile created, False otherwise.
        """
        return self.organizer_service.create_new_settings_profile(
            self.services.blackboards.services_blackboard.DEFAULT_SETTINGS_TYPE,
            new_settings_profile_name, data)

    def save_settings_profile(self, settings_profile_name: str) -> bool:
        """
        Save the specified settings profile.
        Note that the specified profile must exist.

        Args:
            settings_profile_name (str): Name of the profile.

        Returns:
            (bool):
                True if the  profile is successfully saved to disk,
                False otherwise.
        """
        return self.organizer_service.save_settings_profile(
            settings_profile_name)

    def remove_settings_profile(self, settings_profile_name: str) -> bool:
        """
        Remove the specified settings profile.
        Note that this removes the profile from disk, if saved.

        Args:
            settings_profile_name (str): Name of the profile.

        Returns:
            (bool): True if the profile is removed successfully, False otherwise.
        """
        return self.organizer_service.remove_settings_profile(
            settings_profile_name)

    def remove_all_settings_profile(self) -> bool:
        """
        Remove all the settings profiles.
        Note that this removes the profile from disk, if saved.

        Returns:
            (bool): True if all profiles are removed, False otherwise.
        """
        return self.organizer_service.remove_all_settings_profiles()

    def change_settings_profile_name(self, settings_profile_name: str,
                                     new_name: str) -> bool:
        """
        Change the name of the specified settings profile to a new name.
        Note that the settings profile must exist and there must not be an
        existing profile with the new name.

        Args:
            settings_profile_name (str): Name of the profile.
            new_name (str): The profile name is changed to this.
        """
        return self.organizer_service.change_settings_profile_name(
            settings_profile_name, new_name)

    def apply_settings_profile_to_source(self, source_name: str,
                                         settings_profile_name: str) -> bool:
        """
        Apply the specified, existing settings profile to this specified,
        existing source.

        Args:
            source_name (str)
            settings_profile_name (str)

        Returns:
            (bool):
            True if the profile is applied to the source, False otherwise.
        """
        return self.organizer_service.apply_settings_profile_to_source(
            source_name, settings_profile_name)

    def apply_settings_profile_to_sources(self, source_names: List[str],
                                          settings_profile_name: str) -> bool:
        """
        Apply the specified settings profile to the specified sources.
        Note that the sources and settings profile must exist.

        Args:
            source_names (List[str]): Names of multiple sources.
            settings_profile_name (str)

        Returns:
            (bool): True if the specified profile is applied to all
                    the specified sources.
        """
        return self.organizer_service.apply_settings_profile_to_sources(
            source_names, settings_profile_name)

    def save_source_settings_profile(self, source_name: str,
                                     new_settings_profile_name: str) -> bool:
        """
        Save the settings profile attached to this source to disk.
        This is useful if the settings profile attributes for the specified
        source differ from any existing profiles.

        Args:
            source_name (str)
            new_settings_profile_name (str):
                Name for the new profile. Must be unique.

        Returns:
            (bool): True if the profile is saved, False otherwise.
        """
        return self.organizer_service.save_source_settings_profile(
            source_name, new_settings_profile_name)

    def register_plugins(self, config_path: str) -> List[str]:
        """
        Register analysis plugins from the specified configuration file.

        Args:
            config_path (str): Path to the configuration file.

        Returns:
            (List[str]): List of plugins loaded using the configuration file.
        """
        return self.pipeline.register_plugins(config_path)

    def transcribe(self) -> Any:
        """
        Transcribe sources that are ready to transcribe.

        Returns:
            (PipelineServiceSummary)
        """
        return self.pipeline.execute(
            self.organizer_service.get_configured_sources())

    ############################### GETTERS #################################

    def get_supported_source_formats(self) -> List[str]:
        """
        Obtain a list of supported audio formats.

        Returns:
            (List[str]): Supported audio formats.
        """
        pass

    def is_source(self, source_name: str) -> bool:
        """
        Determine if a source with the specified source name exists.

        Args:
            source_name (str)

        Returns:
            (bool: True if the source exists, False otherwise.
        """
        return self.organizer_service.is_source(source_name)

    def is_source_ready_to_transcribe(self, source_name: str) -> bool:
        """
        Determine if the specified source is ready to transcribe.

        Args:
            source_name (str)

        Returns:
            (bool): True if the specified source is ready to transcribe,
                    False otherwise.
        """
        return self.organizer_service.is_source_configured(source_name)

    def get_source_names(self) -> List[str]:
        """
        Obtain the names of all added sources.

        Returns:
            (List[str]): Names of sources
        """
        return self.organizer_service.get_source_names()

    def get_names_of_sources_ready_to_transcribe(self) -> List[str]:
        """
        Obtain the names of sources that are ready to transcribe.

        Returns:
            (List[str]): Names of sources
        """
        return self.organizer_service.get_configured_source_names()

    def get_source_details(self, source_name: str) -> SourceDetails:
        """
        Obtain the SourceDetails for the specified source.

        Args:
            source_name (str)

        Returns:
            (SourceDetails)
        """
        return self.organizer_service.get_source_details(source_name)

    def get_sources_details(self, source_names: List[str]) \
            -> Dict[str, SourceDetails]:
        """
        Obtain a mapping from the source names to their SourceDetails.

        Args:
            source_names (List[str]): Names of all sources.

        Returns:
            (Dict[str,SourceDetails]):
                Mapping from source names to their SourceDetails.
        """
        return self.organizer_service.get_sources_details(source_names)

    def get_all_source_details(self) -> Dict[str, SourceDetails]:
        """
        Obtain a mapping from source names to SourceDetails for all sources.

        Returns:
            (Dict[str,SourceDetails]):
                Mapping from source names to their SourceDetails.
        """
        return self.organizer_service.get_all_source_details()

    def is_settings_profile(self, settings_profile_name: str) -> bool:
        """
        Determine if the settings profile exists.

        Args:
            settings_profile_name (str): Name of the settings profile.

        Returns:
            (bool): True if the profile exists, False otherwise.
        """
        return self.organizer_service.is_settings_profile(settings_profile_name)

    def is_settings_profile_saved(self, settings_profile_name: str) -> bool:
        """
        Determine if the settings profile is saved to disk.

        Args:
            settings_profile_name (str)

        Returns:
            (bool): True if profile is saved on disk, False otherwise.
        """
        return self.organizer_service.is_settings_profile_saved(
            settings_profile_name)

    def get_settings_profile_details(self, settings_profile_name: str) \
            -> SettingsDetails:
        """
        Get the details for the specified settings profile.
        The profile must exist.

        Args:
            settings_profile_name (str)

        Returns:
            (SettingsDetails)
        """
        return self.organizer_service.get_settings_profile_details(
            settings_profile_name)

    def get_settings_profiles_details(
            self, settings_profile_names: List[str]) -> Dict[str, SettingsDetails]:
        """
        Obtain a mapping from the specified settings profiles to their
        SettingsDetails.
        Note that the result map contains only existing settings profiles.

        Args:
            settings_profile_names (List[str]): Names of the settings profiles.

        Returns:
            (Dict[str,SettingsDetails]):
                Mapping from existing settings details to their SettingsDetails.

        """
        return self.organizer_service.get_settings_profiles_details(
            settings_profile_names)

    def get_all_settings_profiles_details(self) -> Dict[str, SettingsDetails]:
        """
        Obtain a mapping from all the specified settings profiles to their
        SettingsDetails.

        Returns:
            (Dict[str,SettingsDetails]):
                Mapping from existing settings details to their SettingsDetails.
        """
        return self.organizer_service.get_all_settings_profiles_details()

    def get_source_settings_profile_name(self, source_name: str) -> str:
        """
        Obtain the name of the settings profile associated with the specified
        source, if any.

        Args:
            source_name (str)

        Returns:
            (str): Settings profile name, if any.
        """
        return self.organizer_service.get_source_settings_profile_name(
            source_name)

    def get_source_names_using_settings_profile(
            self,  settings_profile_name: str) -> List[str]:
        """
        Obtain the names of all sources using the specified settings profile.
        Note that the settings profile must exist.

        Args:
            settings_profile_name (str)

        Returns:
            (List[str]): Names of all sources using settings profile.
        """
        return self.organizer_service.get_source_names_using_settings_profile(
            settings_profile_name)

    def get_sources_details_using_settings_profile(
            self, settings_profile_name: str) -> Dict[str, SourceDetails]:
        """
        Obtain a map from source name to the associated SourceDetails for
        all sources using the specified settings profile.
        Note that the settings profile must exist.

        Args:
            settings_profile_name (str)

        Returns:
            (Dict[str,SourceDetails]):
                Map from source name to SourceDetails.
        """
        return self.organizer_service.get_sources_details_using_settings_profile(
            settings_profile_name)

    def get_source_settings_profile_details(self, source_name: str) \
            -> SettingsDetails:
        """
        Obtain the SettingsDetails, of the settings profile associated with the
        specified source, if any.
        Note that the source must exist.

        Args:
            source_name (str)

        Returns:
            (SettingsDetails)
        """
        return self.organizer_service.get_source_settings_profile_details(
            source_name)

    def get_sources_settings_profile_details(self, source_names: List[str]) \
            -> Dict[str, SettingsDetails]:
        """
        Obtain a mapping from source names to the SettingsDetails for their
        settings profile, if any.

        Args:
            source_names (List[str]): Names of the sources.

        Returns:
            (Dict[str,SettingsDetails]):
                Map from source name to SettingsDetails
        """
        return self.organizer_service.get_sources_settings_profile_details(
            source_names)

    def get_all_sources_settings_profile_details(self) \
            -> Dict[str, SettingsDetails]:
        """
        Obtain a mapping from all sources to the SettingsDetails for their
        settings profile, if any.

        Returns:
            (Dict[str,SettingsDetails]):
                Map from source name to SettingsDetails
        """
        return self.organizer_service.get_all_settings_profiles_details()

    def get_plugin_names(self) -> List[str]:
        """
        Obtain the names of all registered analysis plugins.

        Returns:
            (List[str])
        """
        return self.pipeline.get_plugin_names()

    ############################## SETTERS ###################################

    def set_settings_profile_attribute(self, settings_profile_name: str,
                                       attr: GBSettingAttrs, value: Any) -> bool:
        """
        Set a value for the specified attribtue for the specified
        settings profile.
        Note that the profile must exist.

        Args:
            settings_profile_name (str)
            attr (GbSettingAttrs)
            value (Any)

        Returns:
            (bool): True if the attribute is set successfully, False otherwise.
        """
        return self.organizer_service.set_settings_profile_attribute(
            settings_profile_name, attr, value)

    def set_source_settings_profile_attribute(
            self, source_name: str,  attr: GBSettingAttrs, value: Any) -> bool:
        """
        Set a value for the specified attribute for the specified source.
        Note that this sets the attribute for the source only, and not for the
        entire settings profile associated with the source.
        Note that the source must exist.

        Args:
            source_name (str)
            attr (GBSettingAttrs)
            value (Any)

        Returns:
            (bool): True if set successfully, False otherwise.
        """
        return self.organizer_service.set_source_settings_profile_attribute(
            source_name, attr, value)
