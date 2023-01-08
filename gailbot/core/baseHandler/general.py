# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 16:28:03
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-08 16:46:11


from typing import Any, Callable, Tuple, List, Dict
import os
import glob
import json
import yaml
import shutil
import itertools
from pathlib import Path
# Local imports
# Third party imports
from copy import deepcopy
from .types import dtype


class GeneralIO:
    """
    Provides methods that deal with reading and writing non-media files and
    interacting with the file system.
    """
    def __init__(self):
        pass

    ############################## INSPECTORS ###############################

    def get_size(self, path : str) -> bytes:
        """Size of file or dir. """
        if os.path.isfile(path):
            return os.path.getsize(path)
        paths = self.get_path_items_in_dir(path,["*"])
        return sum([os.path.getsize(p) for p in paths])

    def get_name(self, path : str) -> str:
        """Name of file or dir"""
        return os.path.splitext(os.path.basename(path))[0]

    def get_extension(self, path : str) -> str:
        return os.path.splitext(os.path.basename(path))[1]

    def get_parent_path(self, path : str) -> str:
        return Path(path).parent.absolute()

    def is_directory(self, dir_path: str) -> bool:
        """
        Determine if the given path is a directory.
        """
        return os.path.exists(dir_path) and os.path.isdir(dir_path)

    def is_file(self, file_path: str) -> bool:
        """
        Determine if the given path is a file.
        """
        return os.path.exists(file_path) and os.path.isfile(file_path)


    def get_path_items_in_dir(
        self,
        path: str,
        extensions: List[str],
        check_subdirectories: bool = True,
        only_dirs : bool = False
    ) -> List[str]:
        """
        Determine the paths, relative to dir_path, of all files in the
        directory.
        Args:
            dir_path (str): Path to directory.
            extensions (List[str]): Specific file extensions to look for.
                        Ex: ["pdf"]. '*' is a wildcard and considers all
                        extensions. Does not consider sub-directories.
                        default = ["*"]
            check_subdirectories (bool): True to check subdirectories.
                                        False otherwise. default = False
            only_dirs (bool): Only applies to dirs.
        """
        if not self.is_directory(path):
            raise Exception(f"ERROR: Not a directory")
        if only_dirs:
            return glob.glob(f"{path}/**",recursive=check_subdirectories)
        else:
            return itertools.chain(
                *[glob.glob(f"{path}/*.{ext}",recursive=check_subdirectories) for \
                    ext in extensions]
            )

    def get_num_items_in_dir(
        self,
        path: str,
        extensions: List[str],
        check_subdirectories: bool = False,
        only_dirs : bool = False
    ) -> int:
        """
        Determine the number of files in the directory.
        Args:
            dir_path (str): Path to directory.
            extensions (List[str]): Specific file extensions to look for.
                        Ex: ["pdf"]. '*' is a wildcard and considers all
                        extensions. Does not consider sub-directories.
                        default = ["*"]
            check_subdirectories (bool): True to check subdirectories.
                                False otherwise. default = False
            only_dirs (bool): Only applies to dirs.
        """

        return len(self.get_path_items_in_dir(
            path, extensions,check_subdirectories,only_dirs
        ))


