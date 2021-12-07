# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-11-05 21:07:36
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2021-12-07 11:54:02
# Standard imports
from typing import List, Any, Dict

# Local imports
from ..organizer_service import OrganizerService
from ..pipeline_service import PipelineService
from ..shared_models import Settings, GailBotSettings


class GailBotController:
    """
    Provides an API to use GailBot.
    """

    def __init__(self, workspace_dir_path: str) -> None:
        self.organizer_service = OrganizerService(workspace_dir_path)
        self.pipeline_service = PipelineService()

    ############################### MODIFIERS ###############################

    def shutdown(self) -> None:
        """
        Shutdown the controller components properly.
        """
        pass

    def add_source(self, source_name: str, source_path: str,
                   result_dir_path: str) -> bool:
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
            source_name, source_path, result_dir_path)

    def remove_source(self, source_name: str) -> bool:
        """
        Remove a source that has been added.

        Args:
            source_name (str): Name of the source.

        Returns:
            (bool): True if removed successfully, False otherwise.
        """
        return self.organizer_service.remove_source(source_name)

    def reset_source(self, source_name: str) -> bool:
        """
        Reset the specified source, removing any attached settings profiles.

        Args:
            source_name (str): Name of the source.

        Returns:
            (bool): True if successfully reset, False otherwise.
        """
        return self.organizer_service.reset_source(source_name)

    def create_new_settings_profile(self, new_settings_profile_name: str,
                                    data) -> bool:
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
            new_settings_profile_name, data)

    def load_settings_profile(self, path: str) -> bool:
        return self.organizer_service.load_settings_profile(path)

    def save_settings_profile(self, settings_profile_name: str) -> str:
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
            source_name, settings_profile_name
        )

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
        return self.pipeline_service.register_plugins(config_path)

    def transcribe(self) -> Any:
        """
        Transcribe sources that are ready to transcribe.

        Returns:
            (PipelineServiceSummary)
        """
        self.pipeline_service.execute(
            self.organizer_service.get_configured_sources())

    ############################### GETTERS #################################

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

    def get_settings_profile_names(self) -> List[str]:
        return self.organizer_service.get_settings_profile_names()

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

    def get_plugin_names(self) -> List[str]:
        """
        Obtain the names of all registered analysis plugins.

        Returns:
            (List[str])
        """
        pass

    def get_settings_profile(self, settings_profile_name) -> GailBotSettings:
        return self.organizer_service.get_settings_profile(
            settings_profile_name)

    def get_source_settings_profile(self, source_name) -> GailBotSettings:
        return self.organizer_service.get_source_settings_profile(
            source_name)

    ############################## SETTERS ###################################
