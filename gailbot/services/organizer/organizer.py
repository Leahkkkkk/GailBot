# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 13:48:55
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-16 14:58:17

from typing import Union, List, Dict, Any
from gailbot.plugins import PluginManager, Plugin, PluginSuite
from .sourceManager import SourceManager
from .settingsManager import SettingsManager
from .objects import Settings, Source

# TODO: Look into using an ORM to manage the underlying objects, such as marshmallow.

class OrganizerService:

    def __init__(
        self,
        sources_ws : str,
        settings_ws : str
    ):
        self.source_manager = SourceManager(sources_ws)
        self.settings_manager = SettingsManager(settings_ws)


    ## SourceManager

    def add_source(
        self,
        source_name : str,
        source_path : str
    ) -> bool:
        return self.source_manager.add_source(
            source_name, source_path
        )

    def remove_source(self, source_name : str) -> bool:
        return self.source_manager.remove_source(source_name)

    def is_source(self, source_name : str) -> bool:
        return self.source_manager.is_source(source_name)

    def is_source_configured(self, source_name : str) -> bool:
        if not self.source_manager.is_source(source_name):
            return False
        source = self.source_manager.get_source(source_name)
        return source.settings_profile != None

    def source_names(self) -> List[str]:
        return self.source_manager.source_names()

    def get_source_details(self, source_name : str) -> Dict:
        return self.source_manager.get_source_details(source_name)

    def get_source(self, source_name : str) -> Source:
        if self.is_source(source_name):
            return self.source_manager.get_source(source_name)

    ## SettingsManager

    def create_new_settings_profile(
        self,
        profile_name: str,
        data : Union[str, Dict]
    ) -> bool:
        """Create profile from a config file """
        return self.settings_manager.create_new_settings_profile(
            profile_name, data
        )

    def save_settings_profile(
        self,
        profile_name : str,
        output_dir : str
    ) -> bool:
        return self.settings_manager.save_settings_profile(
            profile_name, output_dir
        )

    def load_settings_profile(self, file_path : str) -> bool:
        return self.settings_manager.load_settings_profile(file_path)

    def remove_settings_profile(self, profile_name : str) -> bool:
        return self.settings_manager.remove_settings_profile(profile_name)

    def change_profile_name(
        self,
        profile_name : str,
        new_name : str
    ) -> bool:

        source_names = self.get_sources_using_settings_profile(profile_name)
        if self.settings_manager.change_profile_name(
                profile_name, new_name):
            for name in source_names:

                source = self.source_manager.get_source(name)

                if not self.apply_settings_profile_to_source(
                        source.identifier,new_name):
                    return False
            return True
        return False

    def is_settings_profile(self, profile_name : str) -> bool:
        return self.settings_manager.is_settings_profile(profile_name)

    def get_profile_names(self) -> List[str]:
        return self.settings_manager.get_profile_names()

    def get_settings_profile_details(self, profile_name : str) -> Dict:
        return self.settings_manager.get_settings_profile_details(profile_name)

    #### Methods for interaction b/w sources and settings

    def apply_settings_profile_to_source(
        self,
        source_name : str,
        profile_name : str
    ) -> bool:
        if not self.source_manager.is_source(source_name) or \
                not self.settings_manager.is_settings_profile(profile_name):
            return False
        settings = self.settings_manager.get_settings_profile(profile_name)
        source = self.source_manager.get_source(source_name)
        source.settings_profile = settings
        return True

    def remove_settings_profile_from_source(
        self,
        source_name : str,
        profile_name : str
    ) -> bool:
        if not self.source_manager.is_source(source_name) or \
                not self.settings_manager.is_settings_profile(profile_name):
            return False
        source = self.source_manager.get_source(source_name)
        source.settings_profile = None
        return True

    def get_sources_using_settings_profile(
        self,
        profile_name : str
    ) -> List[str]:
        res = self.source_manager.map_sources(
            lambda source : source.settings_profile.name == profile_name,
        )
        return [name for name, value in res.items() if value]

    def get_source_settings_profile(self, source_name : str) -> Settings:
        if not self.source_manager.is_source(source_name):
            return
        source = self.source_manager.get_source(source_name)
        return source.settings_profile





