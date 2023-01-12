# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 16:28:03
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-12 14:55:17


from typing import Any, Callable, Tuple, List, Dict
import os
import glob
import json
import yaml
import toml
import shutil
import itertools
from pathlib import Path
# Local imports
# Third party imports
from copy import deepcopy


def is_directory(dir_path: str) -> bool:
    """
    Determine if the given path is a directory.
    """
    return os.path.exists(dir_path) and os.path.isdir(dir_path)

def is_file(file_path: str) -> bool:
    """
    Determine if the given path is a file.
    """
    return os.path.exists(file_path) and os.path.isfile(file_path)

def num_items_in_dir(
    path: str,
    extensions: List[str],
    recursive: bool = False,
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

    return len(paths_in_dir(
        path, extensions,recursive,only_dirs
    ))


def paths_in_dir(
    path: str,
    extensions: List[str],
    recursive: bool = True,
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
    if not is_directory(path):
        raise Exception(f"ERROR: Not a directory")
    if only_dirs:
        return glob.glob(f"{path}/**",recursive=recursive)
    else:
        return itertools.chain(
            *[glob.glob(f"{path}/*.{ext}",recursive=recursive) for \
                ext in extensions]
        )

def filepaths_in_dir(
    dir_path : str,
    extensions : List[str] = ["*"],
    recursive : bool = False
) -> List[str]:
    """
    Get paths of files with specified extension in dir.
    Raise Exception if dir_path not a dir
    """
    pass

def subdirs_in_dir(
    dir_path : str,
    recursive : bool = False
) -> List[str]:
    """
    Get paths of subdirs with specified extension in dir.
    Raise Exception if dir_path not a dir
    """
    pass

def num_subdirs(dir_path : str, recursive : bool = False) -> int:
    """Get num subdirs in dir"""
    pass

def get_name(path : str) -> str:
    """Name of file or dir"""
    return os.path.splitext(os.path.basename(path))[0]

def get_extension(path : str) -> str:
    return os.path.splitext(os.path.basename(path))[1]

def get_parent_path(path : str) -> str:
    return Path(path).parent.absolute()

def get_size(path : str) -> bytes:
    """Size of file or dir. """
    pass

def make_dir(path : str, overwrite : bool = False):
    pass

def move(src_path : str, tgt_path : str) -> str:
    pass

def copy(src_path, tgt_path : str) -> str:
    pass

def rename(src_path, new_name : str) -> str:
    pass

def delete(path : str) -> bool:
    pass

def read_json(path : str) -> Dict:
    pass

def write_json(path : str, data : Dict, mode : str) -> bool:
    pass

def read_txt(path : str) -> List:
    pass

def write_text(path : str, data : List, mode : str) -> bool:
    pass

def read_yaml(path : str) -> Dict:
    pass

def write_yaml(path : str, data : Dict, mode : str) -> bool:
    pass

def read_toml(path : str) -> Dict:
    return toml.load(path)

def write_toml(path : str, data : Dict, mode : str) -> bool:
    pass

def run_cmd(
    cmd : str,
    stdin : Any,
    stdout : Any,
    on_start : Callable,
    on_end : Callable
) -> str:
    """
    Run the command as a shell command and obtain an identifier.
    The identifier can be used to obtain the shell command  status using
    get_shell_process_status.
    """
    pass

def get_cmd_status(identifier : str) -> str:
    """
    Obtain the status of the shell command associated with this identifier
    """
    pass