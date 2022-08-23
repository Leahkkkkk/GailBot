# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-02 13:31:04
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-08-23 11:33:49
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any
from gailbot.core.io import GailBotIO


class Settings(ABC):
    pass

    @abstractmethod
    def to_dict(self) -> Dict:
        pass

    @abstractmethod
    def load_from_dict(self, data: Dict) -> bool:
        pass


class SettingsHook:

    SAVE_EXTENSION = "json"

    def __init__(self, settings_profile_name: str,
                 save_dir_path: str, settings: Settings) -> None:
        """
        Args:
            settings_profile_name(str)
            parent_dir_path(str): Directory in which the hook is created.
        """
        self.io = GailBotIO()
        self.settings_profile_name = settings_profile_name
        self.save_dir_path = save_dir_path
        self.save_path = "{}/{}.{}".format(
            save_dir_path, settings_profile_name,
            self.SAVE_EXTENSION)
        self.settings = settings

    ################################## MODIFIERS #############################

    def get_save_path(self) -> str:
        """
        Obtain the save location for this profile.
        """
        return self.save_path

    def set_settings_profile_name(self, name: str) -> None:
        self.settings_profile_name = name
        self.save_path = "{}/{}.{}".format(
            self.save_dir_path, self.settings_profile_name, self.SAVE_EXTENSION)

    def save(self, profile_name: str = None) -> bool:
        """
        Save the settings on disk.
        """
        try:
            if profile_name != None:
                self.save_path = "{}/{}.{}".format(
                    self.save_dir_path, profile_name, self.SAVE_EXTENSION)
            return self.io.write(self.save_path, self.settings.to_dict(), True)
        except Exception as e:
            print(e)
            return False

    def load(self, path: str) -> bool:
        """
        Load a settings profile data form disk.
        """
        if not self.io.is_file(path):
            return False
        # Read and parse
        success, data = self.io.read(path)
        if not success:
            return False
        return self.settings.load_from_dict(data)

    def cleanup(self) -> None:
        """
        Cleanup the hook, removing all files inside the hook.
        """
        # Delete the saved file
        self.io.delete(self.save_path)

    ################################## GETTERS ###############################

    def is_saved(self) -> bool:
        """
        Determine if the settings is saved on disk.
        """
        return self.io.is_file(self.save_path)


@ dataclass
class SettingsProfile:
    name: str
    settings: Settings
    hook: SettingsHook
