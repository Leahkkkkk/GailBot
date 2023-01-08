# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 15:35:55
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-08 16:24:03

from typing import Union, Dict, Any, List
from core.engines.engine import Engine
from plugins import PluginManager
from .organizer import OrganizerService
from .pipeline import PipelineService
from .baseObjects import Source, Settings, Payload

class GailBotController:

    def __init__(
        self,
        workspace_dir : str
    ):
        self.organizer = OrganizerService()
        self.pipeline = PipelineService()

        # Configure
        self.organizer.configure_workspace(workspace_dir)

    def setup(self):
        pass

    def shutdown(self):
        pass

    ### Organizer Service

    def add_source(
        self,
        source_name : str,
        source_path : str,
        output_dir : str
    ) -> bool:
        return self.organizer.add_source(source_name, source_path,output_dir)

    def remove_source(self, source_name : str) -> bool:
        return self.organizer.remove_source(source_name)

    def is_source(self, source_name : str) -> bool:
        return self.organizer.is_source(source_name)

    def source_names(self, configured : bool = False) -> List[str]:
        return self.organizer.source_names(configured)

    def get_source_details(self, source_name : str) -> Dict:
        return self.organizer.get_source_details(source_name)

    ## SettingsManager

    def create_new_settings_profile(
        self,
        profile_name: str,
        data : Union[str, Dict]
    ) -> bool:
        """Create profile from a config file """
        return self.organizer.create_new_settings_profile(
            profile_name, data
        )

    def save_settings_profile(
        self,
        profile_name : str,
        output_dir : str
    ) -> bool:
        return self.organizer.save_settings_profile(
            profile_name, output_dir
        )

    def load_settings_profile(self, file_path : str) -> Settings:
        return self.organizer.load_settings_profile(file_path)

    def remove_settings_profile(self, profile_name : str) -> bool:
        return self.organizer.remove_settings_profile(profile_name)

    def change_profile_name(
        self,
        profile_name : str,
        new_name : str
    ) -> bool:
        return self.organizer.change_profile_name(profile_name, new_name)

    def get_settings_profile(self, profile_name : str) -> Settings:
        return self.organizer.get_settings_profile(profile_name)

    def is_settings_profile(self, profile_name : str) -> bool:
        return self.organizer.is_settings_profile(profile_name)

    def get_profile_names(self) -> List[str]:
        return self.organizer.get_profile_names()

    def get_settings_profile_details(self, profile_name : str) -> Dict:
        return self.organizer.get_settings_profile_details(profile_name)

    #### Methods for interaction b/w sources and settings

    def apply_settings_profile_to_source(
        self,
        source_name : str,
        profile_name : str
    ) -> bool:
        return self.organizer.apply_settings_profile_to_source(
            source_name, profile_name
        )

    def get_sources_using_settings_profile(
        self,
        profile_name : str
    ) -> List[str]:
        return self.organizer.get_sources_using_settings_profile(
            profile_name
        )

    def get_source_settings_profile(self, source_name : str) -> Settings:
        return self.organizer.get_source_settings_profile(source_name)


    ### Methods for Engines

    def get_engine_instance(
        self,
        engine_name : str,
        config_path : str
    ) -> Engine:
        """
        Get an instance of an engine in case it provides additional
        configurable functionality
        """
        return self.organizer.get_engine_instance(engine_name, config_path)

    ### Pipeline Service

    def run_pipeline(self):
        self.pipeline(self.organizer.get_payloads())

    ### PluginManager

    def register_plugin_suite(
        self,
        suite_name : str,
        source_path : str
    ) -> Dict:
        return self.organizer.register_plugin_suite(suite_name, source_path)

    def get_plugin_suite_details(self, suite_name : str) -> Dict:
        return self.organizer.get_plugin_suite_details(suite_name)









