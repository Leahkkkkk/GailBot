# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-02 13:31:04
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2021-12-02 14:08:05

from dataclasses import dataclass
from typing import Dict, Any
from ..io import IO


@dataclass
class Settings:
    pass


class SettingsHook:

    def __init__(self, settings_profile_name: str,
                 parent_dir_path: str) -> None:
        """
        Args:
            settings_profile_name(str)
            parent_dir_path(str): Directory in which the hook is created.
        """
        self.io = IO()
        self.settings_profile_name = settings_profile_name
        self.parent_dir_path = parent_dir_path

    ################################## MODIFIERS #############################

    def save(self, settings: Settings) -> bool:
        """
        Save the given settings object to the hook.
        Must have a settings.save_to_file method.

        Args:
            settings(Settings)

        Returns:
            (bool): True if successfully saved. False otherwise.
        """
        try:
            return settings.save_to_file(
                "{}/{}".format(self.parent_dir_path, self.settings_profile_name))
        except:
            return False

    def load(self) -> Dict[str, Any]:
        """
        Load a settings profile data from the hook.

        Returns:
            (Dict[str, Any])
        """
        # Load the data from the hook path
        paths = self.io.path_of_files_in_directory(
            self.parent_dir_path, ["*"], False)[1]
        for path in paths:
            if self.io.get_name(path) == self.settings_profile_name:
                success, data = self.io.read(path)
                return data if success else {}
        return {}

    def cleanup(self) -> None:
        """
        Cleanup the hook, removing all files inside the hook.
        """
        paths = self.io.path_of_files_in_directory(
            self.parent_dir_path, ["*"], False)[1]
        for path in paths:
            if self.io.get_name(path) == self.settings_profile_name:
                self.io.delete(path)
    ################################## GETTERS ###############################

    def is_saved(self) -> bool:
        """
        Determine if the settings is saved to the hook.

        Returns:
            (bool): True if the settings is saved, False otherwise.
        """
        paths = self.io.path_of_files_in_directory(
            self.parent_dir_path, ["*"], False)[1]
        for path in paths:
            if self.io.get_name(path) == self.settings_profile_name:
                return True


@dataclass
class SettingsProfile:
    name: str
    settings: Settings
    hook: SettingsHook
