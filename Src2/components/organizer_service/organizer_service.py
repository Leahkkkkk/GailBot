# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-10-19 18:14:54
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2021-12-02 14:56:58

# Standard imports
from typing import List, Dict, Any, Callable, Set
from ..io import IO
from ..shared_models import Source, SourceHook, Settings, SettingsHook,\
    SettingsProfile
from ..utils.manager import ObjectManager
from .source_loader import SourceLoader


class OrganizerService:

    def __init__(self, ws_dir_path: str) -> None:
        self.io = IO()
        self.sources: ObjectManager = ObjectManager()
        self.settings_profiles: ObjectManager = ObjectManager()
        self.source_loader = SourceLoader()

    ############################## MODIFIERS #################################
    # ---- Others

    def add_source(self, source_name: str, source_path: str,
                   result_dir_path: str, transcriber_name: str) -> bool:
        if self.is_source(source_name):
            return False
        source = self.source_loader.load_source(
            source_name, source_path, result_dir_path, transcriber_name)
        return self.sources.add_object(source_name, source) \
            if source != None else False

    def remove_source(self, source_name: str) -> bool:
        pass

    def reset_source(self, source_name: str) -> bool:
        pass

    # Settings profiles

    def create_new_settings_profile(
        self, settings_type: str,
            new_settings_profile_name: str, data) \
            -> bool:
        pass

    def save_settings_profile(self, settings_profile_name: str) -> bool:
        pass

    def remove_settings_profile(self, settings_profile_name: str) -> bool:
        pass

    def change_settings_profile_name(self, settings_profile_name: str,
                                     new_name: str) -> bool:
        pass

    def apply_settings_profile_to_source(self, source_name: str,
                                         settings_profile_name: str) -> bool:
        pass

    def apply_settings_profile_to_sources(self, source_names: List[str],
                                          settings_profile_name: str) -> bool:
        pass

    # Sources and settings profiles.

    def save_source_settings_profile(self, source_name: str,
                                     new_settings_profile_name: str) -> bool:
        pass

    ############################## GETTERS ###################################

    def get_supported_audio_formats(self) -> List[str]:
        pass

    def get_supported_video_formats(self) -> List[str]:
        pass

    # Sources

    def is_source(self, source_name: str) -> bool:
        return self.sources.is_object(source_name)

    def is_source_configured(self, source_name: str) -> bool:
        pass

    def get_source_names(self) -> List[str]:
        pass

    def get_configured_source_names(self) -> List[str]:
        pass

    def get_configured_sources(self) -> List[Source]:
        return list(self.sources.get_all_objects().values())

    # Settings profiles

    def is_settings_profile(self, settings_profile_name: str) -> bool:
        pass

    def is_settings_profile_saved(self, settings_profile_name: str) -> bool:
        pass

    def get_source_settings_profile_name(self, source_name: str) -> str:
        pass

    def get_source_names_using_settings_profile(
            self, settings_profile_name: str) -> List[str]:
        pass

    ############################## SETTERS ###################################

    def set_settings_profile_attribute(self, settings_profile_name: str,
                                       attr: Any, value: Any) -> bool:
        pass

    def set_source_settings_profile_attribute(self, source_name: str,
                                              attr: Any, value: Any) -> bool:
        pass

    ######################### PRIVATE METHODS ###############################

    def _is_source_configurable(self, source_name: str) -> bool:
        pass
