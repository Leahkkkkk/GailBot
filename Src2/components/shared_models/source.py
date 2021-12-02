# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-02 13:31:00
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2021-12-02 14:38:18
from dataclasses import dataclass
from typing import Dict, Any, List
from ..io import IO


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


@dataclass
class DataFile:
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
