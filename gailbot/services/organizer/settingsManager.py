# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 14:50:11
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-08 15:00:45

from typing import Union, List, Dict, Any
from ..baseObjects.objects import Settings

class SettingsManager:

    def __init__(self):
        pass

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



