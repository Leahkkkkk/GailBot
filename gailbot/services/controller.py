# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 15:35:55
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-09 15:56:51

from typing import Union, Dict, Any, List
from core.engines.engine import Engine, Watson
from plugins import PluginManager
from .organizer import OrganizerService, Source, Settings
from .pipeline import PipelineService,Payload

class GailBotController:

    ENGINES = {
        "watson" : Watson
    }

    def __init__(
        self,
        workspace_dir : str
    ):
        self.plugin_manager = PluginManager(f"{workspace_dir}/plugins")
        self.organizer = OrganizerService(f"{workspace_dir}/organizer")
        self.pipeline = PipelineService()

    def setup(self):
        pass

    def reset_workspace(self):
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

    def is_source_ready_to_transcribe(self, source_name : str) -> bool:
        return self.organizer.is_source_configured(source_name)

    def source_names(self) -> List[str]:
        return self.organizer.source_names()

    def get_names_of_sources_ready_to_transcribe(self) -> List[str]:
        return [name for name in self.source_names() if\
             self.organizer.is_source_configured(name)]

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

    def apply_settings_profile_to_sources(
        self,
        source_names : List[str],
        profile_name : str
    ) -> bool:
        return all([self.apply_settings_profile_to_source(
            source_name, profile_name
        ) for source_name in source_names])

    def remove_settings_profile_from_source(
        self,
        source_name : str,
        profile_name : str
    ) -> bool:
        return self.organizer.remove_settings_profile_from_source(
            source_name, profile_name
        )

    def get_sources_using_settings_profile(
        self,
        profile_name : str
    ) -> List[str]:
        return self.organizer.get_sources_using_settings_profile(
            profile_name
        )

    def get_source_settings_profile_name(self, source_name : str) -> str:
        return self.organizer.get_source_settings_profile(source_name).name


    ### Methods for Engines

    def get_engine_instance(
        self, engine_name : str, *args, **kwargs
    ) -> Engine:
        """
        Get an instance of an engine in case it provides additional
        configurable functionality
        """

        if not engine_name in self.ENGINES:
            raise Exception(
                f"Engine { engine_name}not supported, pick from {self.ENGINES.keys()}"
            )

        return self.ENGINES[engine_name](*args, **kwargs)

    ### Pipeline Service

    def transcribe(self):
        # Get the sources that are configured and add to pipeline

        configured_sources = [
            name for name in self.organizer.source_names() \
                if self.organizer.is_source_configured(name)
        ]
        sources = [
            self.organizer.get_source(name) for name in configured_sources
        ]
        payloads = [Payload(source=source) for source in sources]

        return self.pipeline(payloads)

    ### PluginManager

    def register_plugin_suite(
        self,
        suite_name : str,
        source_path : str
    ) -> Dict:
        return self.plugin_manager.register_suite(
            suite_name, source_path
        )

    def get_plugin_suite_details(self, suite_name : str) -> Dict:
        return self.plugin_manager.get_suite_details(suite_name)









