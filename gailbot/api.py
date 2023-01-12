# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-10 14:06:17
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-12 14:38:24

import sys
import os
from typing import List, Dict, Any, Union
from gailbot.core.engines import Engine
from gailbot.services import GailBotController

class GailBot:
    """API Wrapper"""

    def __init__(
        self,
        workspace_dir : str
    ):
        self.gb = GailBotController(workspace_dir)

    def reset_workspace(self):
        self.gb.reset_workspace()
    ### Organizer Service

    def add_source(
        self,
        source_name : str,
        source_path : str,
        output_dir : str
    ) -> bool:
        return self.gb.add_source(source_name, source_path,output_dir)

    def remove_source(self, source_name : str) -> bool:
        return self.gb.remove_source(source_name)

    def is_source(self, source_name : str) -> bool:
        return self.gb.is_source(source_name)

    def is_source_ready_to_transcribe(self, source_name : str) -> bool:
        return self.gb.is_source_configured(source_name)

    def source_names(self) -> List[str]:
        return self.gb.source_names()

    def get_names_of_sources_ready_to_transcribe(self) -> List[str]:
        return self.gb.get_names_of_sources_ready_to_transcribe()

    def get_source_details(self, source_name : str) -> Dict:
        return self.organizer.get_source_details(source_name)

    ## SettingsManager

    def create_new_settings_profile(
        self,
        profile_name: str,
        data : Union[str, Dict]
    ) -> bool:
        """Create profile from a config file """
        return self.gb.create_new_settings_profile(
            profile_name, data
        )

    def save_settings_profile(
        self,
        profile_name : str,
        output_dir : str
    ) -> bool:
        return self.gb.save_settings_profile(
            profile_name, output_dir
        )

    def load_settings_profile(self, file_path : str) -> bool:
        return self.gb.load_settings_profile(file_path)

    def remove_settings_profile(self, profile_name : str) -> bool:
        return self.gb.remove_settings_profile(profile_name)

    def change_profile_name(
        self,
        profile_name : str,
        new_name : str
    ) -> bool:
        return self.gb.change_profile_name(profile_name, new_name)

    def is_settings_profile(self, profile_name : str) -> bool:
        return self.organizer.is_settings_profile(profile_name)

    def get_profile_names(self) -> List[str]:
        return self.gb.get_profile_names()

    def get_settings_profile_details(self, profile_name : str) -> Dict:
        return self.gb.get_settings_profile_details(profile_name)

    #### Methods for interaction b/w sources and settings

    def apply_settings_profile_to_source(
        self,
        source_name : str,
        profile_name : str
    ) -> bool:
        return self.gb.apply_settings_profile_to_source(
            source_name, profile_name
        )

    def apply_settings_profile_to_sources(
        self,
        source_names : List[str],
        profile_name : str
    ) -> bool:
        return self.gb.apply_settings_profile_to_sources(
            source_names, profile_name
        )

    def remove_settings_profile_from_source(
        self,
        source_name : str,
        profile_name : str
    ) -> bool:
        return self.gb.remove_settings_profile_from_source(
            source_name, profile_name
        )

    def get_sources_using_settings_profile(
        self,
        profile_name : str
    ) -> List[str]:
        return self.gb.get_sources_using_settings_profile(profile_name)

    def get_source_settings_profile_name(self, source_name : str) -> str:
        return self.gb.get_source_settings_profile_name(source_name)


    ### Methods for Engines

    def available_engines(self) -> List[str]:
        return self.gb.available_engines()

    def get_engine_instance(
        self, engine_name : str, conf : Dict = None
    ) -> Engine:
        """
        Get an instance of an engine in case it provides additional
        configurable functionality
        """
        return self.gb.init_engine(engine_name,conf)

    ### Pipeline Service

    def transcribe(self):
        # Get the sources that are configured and add to pipeline
        return self.gb.transcribe()

    ### PluginManager

    def register_plugin_suite(
        self,
        suite_name : str,
        source_path : str
    ) -> Dict:
        return self.gb.register_suite(suite_name, source_path)

    def get_plugin_suite_details(self, suite_name : str) -> Dict:
        return self.gb.get_suite_details(suite_name)











