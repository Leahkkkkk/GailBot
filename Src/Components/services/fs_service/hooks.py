# Standard imports
from dataclasses import dataclass
from typing import Dict, Callable, List, Any

from Src.components.organizer import settings
# Local imports
from ...utils.observer import ObserverEventManager, Subscriber
from ...utils.manager import ObjectManager
from ...io import IO
from ...organizer import Settings


class SourceHook:

    def __init__(self, parent_dir_path: str, source_name: str,
                 result_dir_path: str) -> None:
        # Objects
        self.io = IO()
        self.parent_dir_path = parent_dir_path
        self.source_name = source_name
        self.result_dir_path = self._generate_result_dir_path(
            result_dir_path, source_name)
        self.temp_dir_path = "{}/{}".format(parent_dir_path, "temp")
        self.io.create_directory(self.result_dir_path)
        self.io.create_directory(self.temp_dir_path)

    ################################# MODIFIERS #############################

    def save(self) -> None:
        """
        Move the temp directory to the result directpry path.
        """
        if not self.io.is_directory(self.result_dir_path) and \
                not self.io.create_directory(self.result_dir_path):
            return
        paths = self._get_paths_of_items_in_directory(self.temp_dir_path)
        for path in paths:
            self.io.move_file(path, self.result_dir_path)

    def cleanup(self) -> None:
        """
        Cleanup this source hook, removing all items in the hook.
        """
        self.io.delete(self.temp_dir_path)
    ################################## GETTERS ###############################

    def get_result_directory_path(self) -> str:
        return self.result_dir_path

    def get_temp_directory_path(self) -> str:
        return self.temp_dir_path

    ############################### PRIVATE METHODS ##########################

    def _get_paths_of_items_in_directory(self, dir_path: str) -> List[str]:
        paths = list()
        if self.io.is_directory(dir_path):
            _, file_paths = self.io.path_of_files_in_directory(
                dir_path, ["*"], False)
            _, dir_paths = self.io.paths_of_subdirectories(dir_path)
            paths.extend(file_paths)
            paths.extend(dir_paths)
        return paths

    def _generate_result_dir_path(self, dir_path: str, source_name: str) \
            -> str:
        count = 0
        while True:
            path = "{}/{}_{}".format(dir_path, source_name, count)
            if self.io.is_directory(path):
                count += 1
            else:
                self.io.create_directory(path)
                break
        return path


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
        return False

    ############################### PRIVATE METHODS ##########################
