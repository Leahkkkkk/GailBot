# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-02 13:31:00
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-08-23 11:34:05
from dataclasses import dataclass
from typing import Dict, Any, List
from .utt import Utt
from .settings import SettingsProfile
from gailbot.core.io import GailBotIO


class SourceHook:

    def __init__(self, source_name: str, temp_ws_path: str,
                 result_dir_path: str) -> None:
        # Objects
        self.io = GailBotIO()
        # Temp ws for this source
        self.temp_ws_path = "{}/{}".format(temp_ws_path, source_name)
        # Result will make sure there is no conflicting name
        self.result_dir_path = self._generate_result_dir_path(
            result_dir_path, source_name)
        # Create a temp. dir for this source specifically
        self.temp_dir_path = "{}/{}".format(self.temp_ws_path, "temp")
        self.io.create_directory(self.temp_dir_path)

    ################################# MODIFIERS #############################

    def save(self) -> None:
        """
        Move the temp directory to the result directory path.
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
        self.io.delete(self.temp_ws_path)

    ################################## GETTERS ###############################

    def get_result_directory_path(self) -> str:
        return self.result_dir_path

    def get_temp_directory_path(self) -> str:
        return self.temp_dir_path

    ############################### PRIVATE METHODS ##########################

    def _get_paths_of_items_in_directory(self, dir_path: str) -> List[str]:
        paths = list()
        if self.io.is_directory(dir_path):
            file_paths = self.io.path_of_files_in_directory(
                dir_path, ["*"], False)
            dir_paths = self.io.paths_of_subdirectories(dir_path)
            paths.extend(file_paths)
            paths.extend(dir_paths)
        return paths

    def _generate_result_dir_path(self, dir_path: str, source_name: str) \
            -> str:
        result_dir_path = "{}/{}".format(dir_path, source_name)
        if self.io.is_directory(result_dir_path):
            count = 1
            while True:
                path = "{}_{}".format(result_dir_path, count)
                if not self.io.is_directory(path):
                    result_dir_path = path
                    break
                count += 1
        self.io.create_directory(result_dir_path)
        return result_dir_path


@dataclass
class DataFile:
    identifier: str
    path: str = None
    audio_path: str = None
    video_path: str = None


@dataclass
class Conversation:
    data_files: List[DataFile]


@dataclass
class Source:
    identifier: str
    conversation: Conversation
    hook: SourceHook
    settings_profile: SettingsProfile = None
