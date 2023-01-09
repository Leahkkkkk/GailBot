# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 14:50:11
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-09 10:16:23

from typing import Union, List, Dict, Any
from .objects import Settings

class SettingsManager:

    def __init__(self):
        self.settings : Dict[str, Settings] = dict()

    def create_new_settings_profile(
        self,
        profile_name: str,
        # Data can be either the settings dictionary directory or path to file
        data : Union[str, Dict]
    ) -> bool:
        """Create profile from a config file """

        if profile_name in self.settings:
            return False

        if isinstance(data, str):
            # Check file exists and load toml
            data = {}

        obj = Settings(data)
        self.settings[profile_name] = obj
        return True

    def save_settings_profile(
        self,
        profile_name : str,
        output_dir : str
    ) -> bool:

        if not profile_name in self.settings:
            return False
        # Create a toml file to save the settings
        settings = self.settings[profile_name]
        path = f"{output_dir}/{settings.name}.toml"
        # Save the data to path - overwrite if exists

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



