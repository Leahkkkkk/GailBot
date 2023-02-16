# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 14:50:11
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-16 14:46:34

from typing import Union, List, Dict, Any
from gailbot.core.utils.general import (
    read_toml,
    is_file,
    write_toml,
    make_dir,
    filepaths_in_dir,
    get_extension,
    get_name,
    delete
)
from .objects import Settings

SETTINGS_SAVE_FORMAT = "toml"

class SettingsManager:

    def __init__(self, workspace_dir : str):
        self.workspace_dir = workspace_dir
        self.settings : Dict[str, Settings] = dict()
        make_dir(workspace_dir,overwrite=False)
        # Load existing settings from the workspace
        paths = filepaths_in_dir(workspace_dir,SETTINGS_SAVE_FORMAT)
        for path in paths:
            self.load_settings_profile(path)


    def create_new_settings_profile(
        self,
        profile_name: str,
        # Data can be either the settings dictionary directory or path to file
        inp : Union[str, Dict]
    ) -> bool:
        """Create profile from a config file """

        if profile_name in self.settings or \
                (not isinstance(inp, str) and not isinstance(inp,dict)):
            return False

        if isinstance(inp, str) and is_file(inp):
            # Check file exists and load toml
            data = read_toml(inp)
        elif isinstance(inp, dict):
            data = inp
        else:
            raise NotImplementedError()

        path = f"{self.workspace_dir}/{profile_name}.{SETTINGS_SAVE_FORMAT}"
        obj = Settings(profile_name,data,path)
        self.settings[profile_name] = obj

        # All settings profile must be saved to disk
        return self.save_settings_profile(profile_name)

    def load_settings_profile(self, file_path : str) -> bool:
        return self.create_new_settings_profile(get_name(file_path),file_path)

    def save_settings_profile(
        self,
        profile_name : str,
        output_dir : str = None
    ) -> bool:

        if not profile_name in self.settings:
            return False
        # Create a toml file to save the settings
        settings = self.settings[profile_name]
        # Save the data to path - overwrite if exists
        if output_dir != None:
            make_dir(output_dir,overwrite=False)
            path = f"{output_dir}/{profile_name}.{SETTINGS_SAVE_FORMAT}"
        else:
            path = settings.save_path

        write_toml(path, settings.to_dict())
        return True

    def remove_settings_profile(self, profile_name : str) -> bool:
        if not profile_name in self.settings:
            return False
        delete(self.settings[profile_name].save_path)
        del self.settings[profile_name]
        return True

    def change_profile_name(
        self,
        profile_name : str,
        new_name : str
    ) -> bool:
        if not profile_name in self.settings:
            return False
        settings = self.settings[profile_name]
        return self.remove_settings_profile(profile_name) and \
            self.create_new_settings_profile(new_name,settings.to_dict())

    def get_settings_profile(self, profile_name : str) -> Settings:
        if not profile_name in self.settings:
            raise Exception(
                f"ERROR: Profile does not exist: {profile_name}"
            )
        return self.settings[profile_name]

    def is_settings_profile(self, profile_name : str) -> bool:
        return profile_name in self.settings

    def get_profile_names(self) -> List[str]:
        return list(self.settings.keys())

    def get_settings_profile_details(self, profile_name : str) -> Dict:
        if self.is_settings_profile(profile_name):
            return self.settings[profile_name].to_dict()



