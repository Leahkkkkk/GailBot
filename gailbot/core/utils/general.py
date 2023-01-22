# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 16:28:03
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-16 14:39:45


import sys
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
import subprocess


# TODO: All of the methods below need to be tested and error handing should be
# added.

def is_directory(dir_path: str) -> bool:
    """
    Determine if the given path is a directory.
    """
    return Path(dir_path).is_dir()

def is_file(file_path: str) -> bool:
    """
    Determine if the given path is a file.
    """
    return Path(file_path).is_file()

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
        return glob.glob(f"{path}/*/",recursive=recursive)
    else:
        return list(itertools.chain(
            *[glob.glob(f"{path}/*.{ext}",recursive=recursive) for \
                ext in extensions]
        ))

def filepaths_in_dir(
    dir_path : str,
    extensions : List[str] = ["*"],
    recursive : bool = False
) -> List[str]:
    """
    Get paths of files with specified extension in dir.
    Raise Exception if dir_path not a dir
    """
    return paths_in_dir(
        path=dir_path,
        extensions=extensions,
        recursive=recursive,
        only_dirs=False
    )

def subdirs_in_dir(
    dir_path : str,
    recursive : bool = False
) -> List[str]:
    """
    Get paths of subdirs with specified extension in dir.
    Raise Exception if dir_path not a dir
    """
    return paths_in_dir(
        path=dir_path,
        extensions=None,
        recursive=recursive,
        only_dirs=True
    )

def num_subdirs(dir_path : str, recursive : bool = False) -> int:
    """Get num subdirs in dir"""
    return len(subdirs_in_dir(dir_path,recursive))

def get_name(path : str) -> str:
    """Name of file or dir"""
    return os.path.splitext(os.path.basename(path))[0]

def get_extension(path : str) -> str:
    return os.path.splitext(os.path.basename(path))[1][1:]

def get_parent_path(path : str) -> str:
    return str(Path(path).parent.absolute())

def get_size(path : str) -> bytes:
    """Size of file or dir"""
    if is_file(path):
        return os.path.getsize(path)
    else:
        return sum([
            os.path.getsize(p) for p in filepaths_in_dir(path,recursive=True)
        ])

def make_dir(path : str, overwrite : bool = False):
    if is_directory(path) and overwrite:
        delete(path)
    os.makedirs(path,exist_ok=True)

def move(src_path : str, tgt_path : str) -> str:
    return shutil.move(src_path, tgt_path)

def copy(src_path, tgt_path : str) -> str:
    if is_file(src_path):
        return shutil.copy(src_path, tgt_path)
    elif is_directory(src_path):
        return shutil.copytree(src_path, tgt_path,dirs_exist_ok=True)

def rename(src_path, new_name : str) -> str:
    return str(Path(src_path).rename(new_name).resolve())

def delete(path : str) -> None:
    if is_file(path):
        Path(path).unlink(missing_ok=True)
    else:
       shutil.rmtree(path)

def read_json(path : str) -> Dict:
    with open(path, 'r') as f:
        return json.load(f)

def write_json(path : str, data : Dict, overwrite : bool = True) -> None:
    if not overwrite:
        d = read_json(path)
    d.update(data)
    with open(path, "w") as f:
        json.dump(d,f)

def read_txt(path : str) -> List:
    return open(path,"r").read()

def write_text(path : str, data : List,  overwrite : bool = True) -> bool:
    data = str(data)
    mode = 'w' if overwrite else "a"
    with open(path, mode) as f:
        f.write(data)

def read_yaml(path : str) -> Dict:
    with open(path, 'r') as f:
        data = yaml.load(f)
        # Data loaded must be a dictionary
        if not type(data) == dict:
            raise Exception
        return data

def write_yaml(path : str, data : Dict, overwrite : bool = True) -> bool:
    data = dict(data)
    if not overwrite:
        previous_data = read_yaml(path)
        previous_data.update(data)
        previous_data.update(data)
    with open(path, "w") as f:
        # Data must be convertable to a dictionary object to be written to
        # a yaml file.
        yaml.dump(previous_data, f)

def read_toml(path : str) -> Dict:
    return toml.load(path)

def write_toml(path : str, data : Dict) -> bool:
    with open(path, "w") as f:
        toml.dump(data, f)

# TODO: Implement these later using POpen instead.
def run_cmd(
    cmd : str,
) -> None:
    """
    Run the command as a shell command and obtain an identifier.
    The identifier can be used to obtain the shell command  status using
    get_shell_process_status.
    """
    result = subprocess.run(
        cmd,shell=True, capture_output=True
    )
    return result.stdout, result.stderr

def get_cmd_status(identifier : str) -> str:
    """
    Obtain the status of the shell command associated with this identifier
    """
    pass