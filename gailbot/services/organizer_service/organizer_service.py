# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-10-19 18:14:54
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-08-23 11:40:44

# Standard imports
from typing import List
from .source_loader import SourceLoader
from gailbot.core.io import GailBotIO
from gailbot.services.objects import (
    Source,
    SourceHook,
    Settings,
    SettingsHook,
    SettingsProfile,
    GailBotSettings,
)
from gailbot.utils.manager import ObjectManager


class OrganizerService:

    def __init__(self, ws_dir_path: str) -> None:
        self.ws_dir_path = f"{ws_dir_path}/gb_workspace"
        self.temp_ws_path = None
        self.io = GailBotIO()
        self.sources: ObjectManager = ObjectManager()
        self.settings_profiles: ObjectManager = ObjectManager()
        self.source_loader = SourceLoader()
        #  Initialize the workspace
        self._initialize_workspace(self.ws_dir_path)

    ############################## MODIFIERS #################################
    # ---- Others

    def add_source(self, source_name: str, source_path: str,
                   result_dir_path: str) -> bool:
        if self.is_source(source_name):
            return False
        source = self.source_loader.load_source(
            source_name, source_path, result_dir_path,
            self.temp_ws_path)
        return self.sources.add_object(source_name, source) \
            if source != None else False

    def remove_source(self, source_name: str) -> bool:
        return self.sources.remove_object(source_name)

    # Settings profiles

    def create_new_settings_profile(
        self,  new_settings_profile_name: str, data) \
            -> bool:
        # Cannot create settings with existing name
        if self.is_settings_profile(new_settings_profile_name):
            return False
        # Create settings
        settings = GailBotSettings()
        if not settings.load_from_dict(data):
            return False
        hook = SettingsHook(
            new_settings_profile_name, self.settings_ws_path, settings)
        profile = SettingsProfile(
            new_settings_profile_name, settings, hook)
        return self.settings_profiles.add_object(
            new_settings_profile_name, profile)

    def save_settings_profile(self, settings_profile_name: str) -> str:
        if not self.is_settings_profile(settings_profile_name):
            return
        profile: SettingsProfile = self.settings_profiles.get_object(
            settings_profile_name)
        if profile.hook.save():
            return profile.hook.get_save_path()

    def load_settings_profile(self, path: str) -> bool:
        if not self.io.is_file(path):
            return False
        # Infer vars.
        profile_name = self.io.get_name(path)
        # Load
        settings = GailBotSettings()
        hook = SettingsHook(profile_name, self.settings_ws_path, settings)
        if not hook.load(path):
            return False
        # Otherwise add to profiles
        profile = SettingsProfile(profile_name, settings, hook)
        return self.settings_profiles.add_object(profile_name, profile)

    def remove_settings_profile(self, settings_profile_name: str) -> bool:
        # Remove profile from all sources using it
        source_names = self.get_source_names_using_settings_profile(
            settings_profile_name)
        for source_name in source_names:
            self.remove_source(source_name)
        # Remove the actual profile.
        return self.settings_profiles.remove_object(settings_profile_name)

    def change_settings_profile_name(
            self, settings_profile_name: str, new_name: str) -> bool:
        if not self.is_settings_profile(settings_profile_name):
            return False
        settings_profile: SettingsProfile = self.settings_profiles.get_object(
            settings_profile_name)
        # Change the name of the provile and the hook.
        settings_profile.name = new_name
        settings_profile.hook.set_settings_profile_name(new_name)
        # Remove object from settings object and re-add with new name
        self.settings_profiles.remove_object(settings_profile_name)
        self.settings_profiles.add_object(new_name, settings_profile)
        # Change profile for all sources using the original one.
        source_names = self.get_source_names_using_settings_profile(
            settings_profile_name)
        for source_name in source_names:
            if not self.apply_settings_profile_to_source(source_name, new_name):
                return False
        return True

    def apply_settings_profile_to_source(
            self, source_name: str,  settings_profile_name: str) -> bool:
        if not self.is_source(source_name) or \
                not self.is_settings_profile(settings_profile_name):
            return False
        # Deep copy the settings object manually
        profile: SettingsProfile = self.settings_profiles.get_object(
            settings_profile_name)
        new_settings = GailBotSettings()
        if not new_settings.load_from_dict(profile.settings.to_dict()):
            return False
        hook = SettingsHook(profile.name, self.settings_ws_path, new_settings)
        new_profile = SettingsProfile(profile.name, new_settings, hook)
        source: Source = self.sources.get_object(source_name)
        # Apply to source.
        source.settings_profile = new_profile
        return True

    def apply_settings_profile_to_sources(
            self, source_names: List[str], settings_profile_name: str) -> bool:
        for source_name in source_names:
            if not self.apply_settings_profile_to_source(
                    source_name, settings_profile_name):
                return False
        return True

    # Sources and settings profiles.

    def save_source_settings_profile(
            self, source_name: str, new_settings_profile_name: str) -> bool:
        if not self.is_source(source_name):
            return False
        source: Source = self.sources.get_object(source_name)
        # Change the settings profile name for this profile object only.
        source.settings_profile.name = new_settings_profile_name
        source.settings_profile.hook.set_settings_profile_name(
            new_settings_profile_name)
        # Save it.
        if not source.settings_profile.hook.save():
            return False
        # Load the profile with the new name
        return self.load_settings_profile(
            source.settings_profile.hook.get_save_path())

    ############################## GETTERS ###################################

    def get_supported_audio_formats(self) -> List[str]:
        return self.io.get_supported_audio_formats()

    def get_supported_video_formats(self) -> List[str]:
        return self.io.get_supported_video_formats()

    # Sources

    def is_source(self, source_name: str) -> bool:
        return self.sources.is_object(source_name)

    def is_source_configured(self, source_name: str) -> bool:
        if not self.is_source(source_name):
            return False
        source: Source = self.sources.get_object(source_name)
        return source.settings_profile != None

    def get_source_names(self) -> List[str]:
        return self.sources.get_object_names()

    def get_configured_source_names(self) -> List[str]:
        return list(self.sources.get_filtered_objects(
            lambda name, obj: self.is_source_configured(name)).keys())

    def get_configured_sources(self) -> List[Source]:
        return list(self.sources.get_filtered_objects(
            lambda name, obj: self.is_source_configured(name)).values())

    # Settings profiles

    def is_settings_profile(self, settings_profile_name: str) -> bool:
        return self.settings_profiles.is_object(
            settings_profile_name)

    def is_settings_profile_saved(self, settings_profile_name: str) -> bool:
        if not self.is_settings_profile(settings_profile_name):
            return False
        profile: SettingsProfile = self.settings_profiles.get_object(
            settings_profile_name)
        return profile.hook.is_saved()

    def get_settings_profile_names(self) -> List[str]:
        return self.settings_profiles.get_object_names()

    def get_source_settings_profile_name(self, source_name: str) -> str:
        if not self.is_source_configured(source_name):
            return
        source: Source = self.sources.get_object(source_name)
        return source.settings_profile.name

    def get_source_names_using_settings_profile(
            self, settings_profile_name: str) -> List[str]:
        return list(self.sources.get_filtered_objects(
            lambda name, obj: self.get_source_settings_profile_name(name)
            == settings_profile_name).keys())

    def get_settings_profile(self, settings_profile_name) -> Settings:
        if not self.is_settings_profile(settings_profile_name):
            return
        profile: SettingsProfile = self.settings_profiles.get_object(
            settings_profile_name)
        return profile.settings

    def get_source_settings_profile(self, source_name: str) -> Settings:
        if not self.is_source_configured(source_name):
            return
        source: Source = self.sources.get_object(source_name)
        return source.settings_profile.settings

    ############################## SETTERS ###################################

    ######################### PRIVATE METHODS ###############################

    def _initialize_workspace(self, ws_dir_path: str) -> None:
        # Reset the workspace
        if not self.io.is_directory(ws_dir_path):
            if not self.io.create_directory(ws_dir_path):
                raise Exception("Cannot initialize workspace")
        else:
            self.io.clear_directory(self.ws_dir_path)
        # Create the temporary workspace dir inside workspace
        self.temp_ws_path = "{}/temp".format(ws_dir_path)
        if not self.io.create_directory(self.temp_ws_path):
            raise Exception("Cannot initialize workspace")
        # Create the settings workspace dir in the workspace.
        self.settings_ws_path = "{}/settings".format(ws_dir_path)
        if not self.io.create_directory(self.settings_ws_path):
            raise Exception("Cannot initialize workspace")
