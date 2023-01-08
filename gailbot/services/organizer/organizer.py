# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 13:48:55
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-08 15:48:02

from typing import Union, List, Dict, Any
from plugins import PluginManager, Plugin, Suite
from core.engines.engine import Engine
from ..baseObjects import Source, Settings, Payload

# TODO: Look into using an ORM to manage the underlying objects, such as marshmallow.

class OrganizerService:

    def __init__(self):
        pass

    def configure_workspace(
        self,
        workspace_dir : str
    ) -> bool:
        pass

    ## SourceManager

    def add_source(
        self,
        source_name : str,
        source_path : str,
        output_dir : str
    ) -> bool:
        pass

    def remove_source(self, source_name : str) -> bool:
        pass

    def is_source(self, source_name : str) -> bool:
        pass

    def has_profile(self, source_name : str) -> str:
        pass

    def configured_sources(self) -> List[Source]:
        pass

    def configured_source_names(self) -> List[str]:
        pass

    def get_source_details(self, source_name : str) -> Dict:
        pass

    ## SettingsManager

    def create_new_settings_profile(
        self,
        profile_name: str,
        data : Union[str, Dict]
    ) -> bool:
        """Create profile from a config file """
        pass

    def save_settings_profile(
        self,
        profile_name : str,
        output_dir : str
    ) -> bool:
        pass

    def load_settings_profile(self, file_path : str) -> Settings:
        pass

    def remove_settings_profile(self, profile_name : str) -> bool:
        pass

    def change_profile_name(
        self,
        profile_name : str,
        new_name : str
    ) -> bool:
        pass

    def get_settings_profile(self, profile_name : str) -> Settings:
        pass

    def is_settings_profile(self, profile_name : str) -> bool:
        pass

    def get_profile_names(self) -> List[str]:
        pass

    def get_settings_profile_details(self, profile_name : str) -> Dict:
        pass

    #### Methods for interaction b/w sources and settings

    def apply_settings_profile_to_source(
        self,
        source_name : str,
        profile_name : str
    ) -> bool:
        pass

    def get_source_settings_profile_name(self) -> str:
        pass

    def get_sources_using_settings_profile(
        self,
        profile_name : str
    ) -> List[Source]:
        pass

    def get_source_settings_profile(self, source_name : str) -> Settings:
        pass

    def get_payloads(self) -> List[Payload]:
        pass

    ### Methods for Engines

    def get_engine_instance(self) -> Engine:
        """
        Get an instance of an engine in case it provides additional
        configurable functionality
        """
        pass



