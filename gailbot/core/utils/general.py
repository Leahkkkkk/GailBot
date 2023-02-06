# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 16:28:03
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-16 14:39:45


from enum import Enum 
import sys
import psutil
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

InvalidPathError = "Error: invalid path"

class CMD_STATUS(Enum):
    RUNNING = 0 
    FINISHED = 1 
    STOPPED = 2
    ERROR = 3
    NOTFOUND = 4
    
def is_directory(dir_path: str) -> bool:
    """
    Determine if the given path is a directory.
    """
    try:
        return Path(dir_path).is_dir()
    except:
        raise Exception(InvalidPathError)

def is_file(file_path: str) -> bool:
    """
    Determine if the given path is a file.
    """
    try:
        return Path(file_path).is_file()
    except:
        raise Exception(InvalidPathError)

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
    try: 
        return len(paths_in_dir(
            path, extensions,recursive, only_dirs
        ))
    except:
        raise Exception(InvalidPathError)


def paths_in_dir(
    path: str,
    extensions: List[str] = ["*"],
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
    try:
        return paths_in_dir(
            path=dir_path,
            extensions=extensions,
            recursive=recursive,
            only_dirs=False
        )
    except: 
        raise Exception(InvalidPathError)

def subdirs_in_dir(
    dir_path : str,
    recursive : bool = False
) -> List[str]:
    """
    Get paths of subdirs with specified extension in dir.
    Raise Exception if dir_path not a dir
    """
    try: 
        return paths_in_dir(
            path=dir_path,
            extensions=None,
            recursive=recursive,
            only_dirs=True
        )
    except:
        raise Exception(InvalidPathError)

def num_subdirs(dir_path : str, recursive : bool = False) -> int:
    """Get the number of subdirectory in the dir_path"""
    try:
        return len(subdirs_in_dir(dir_path,recursive))
    except:
        raise Exception(InvalidPathError)
        

def get_name(path : str) -> str:
    """given the path return the name of file or dir without extension"""
    try: 
        return os.path.splitext(os.path.basename(path))[0]
    except:
        raise Exception(InvalidPathError)
        

def get_extension(path : str) -> str:
    """ given the path to the file, return the extension of the file """
    try: 
        return os.path.splitext(os.path.basename(path))[1][1:]
    except:
        raise Exception(InvalidPathError)


def get_parent_path(path : str) -> str:
    """ given the path to the file, returns the path to the file's 
        parent directory"""
    try:
        return str(Path(path).parent.absolute())
    except:
        raise Exception(InvalidPathError)


def get_size(path : str) -> bytes:
    """given the path to the file, return the file size"""
    try:
        if is_file(path):
            return os.path.getsize(path)
        else:
            return sum([
                os.path.getsize(p) for p in filepaths_in_dir(path,recursive=True)
            ])
    except:
        raise Exception(InvalidPathError)
        

def make_dir(path : str, overwrite : bool = False):
    """ given the path, create a directory """
    try:
        if is_directory(path) and overwrite:
            delete(path)
        os.makedirs(path, exist_ok=True)
    except:
        raise Exception("Fail to create a directory")
        

def move(src_path : str, tgt_path : str) -> str:
    """ move the file from the source path to the target path """
    try:
        return shutil.move(src_path, tgt_path)
    except:
        raise Exception(InvalidPathError)
        
        
def copy(src_path, tgt_path : str) -> str:
    """ copy the file from the source path to the target path """
    if is_file(src_path):
        return shutil.copy(src_path, tgt_path)
    elif is_directory(src_path):
        return shutil.copytree(src_path, tgt_path,dirs_exist_ok=True)
    else:
        raise Exception(InvalidPathError)
        
        

def rename(src_path, new_name : str) -> str:
    """ rename the file in the source path to the new name """
    try:
        return str(Path(src_path).rename(new_name).resolve())
    except:
        raise Exception(InvalidPathError)
    
def delete(path : str) -> None:
    """ given a path, delete the file """
    if is_file(path):
        Path(path).unlink(missing_ok=True)
    elif is_directory(path):
        shutil.rmtree(path)
    else:
        raise Exception(InvalidPathError)

def read_json(path : str) -> Dict:
    """ given a path, read the json data stored in the file, return the 
        a dictionary that stores the json data 
    """
    if is_file(path):
        with open(path, 'r') as f:
            return json.load(f)
    else:
        raise Exception(InvalidPathError)

def write_json(path : str, data : Dict, overwrite : bool = True) -> None:
    """ given the path to a file and a dictionary, output the data to the  
        given file in the json format
    """
    if not overwrite:
        d = read_json(path)
        d.update(data)
    else: 
        d = data
    try:
        with open(path, "w+") as f:
            json.dump(d,f)
    except Exception as e:
        raise Exception(e)

def read_txt(path : str) -> List:
    """ given the path to a file, return the content of file as a string
    """
    if is_file(path):
        with open(path, "r") as f:
            text = f.readlines()
        text = [s.strip() for s in text]
        return text
    else:
        raise Exception(InvalidPathError)

def write_txt(path : str, data : List,  overwrite : bool = True) -> bool:
    """ given the path to a file, and a list of data, output the list 
        data to the file
    """
    mode = 'w+' if overwrite else "a"
    data = [s + "\n" for s in data]
    try:
        with open(path, mode) as f:
                f.writelines(data)
    except:
        raise Exception(InvalidPathError)
        
def read_yaml(path : str) -> Dict:
    """ given a path to a yaml file, return a dictionary 
        representation of the data stored in the yaml file 
    """
    if is_file(path):
        with open(path, 'r') as f:
            data = yaml.load(f, Loader=yaml.Loader)  # NOTE: added the required parameter Loader
            # Data loaded must be a dictionary
            if not type(data) == dict:
                raise Exception
            return data
    else:
        raise Exception(InvalidPathError)

def write_yaml(path : str, data : Dict, overwrite : bool = True) -> bool:
    """ given a path to a yaml file and data stored in a dictionary,
        output the data in the yaml format to the file
    """
    data = dict(data)
    if not overwrite:
        previous_data = read_yaml(path)
        previous_data.update(data)
        previous_data.update(data)
    else:
        previous_data = data
    try:
        with open(path, "w+") as f:
            # Data must be convertable to a dictionary object to be written to
            # a yaml file.
            yaml.dump(previous_data, f)
    except:
        raise Exception(InvalidPathError)

def read_toml(path : str) -> Dict:
    """ given the path to a to toml file, return a dictionary 
        representation of the data stored in the toml file
    """
    if is_file(path):
        return toml.load(path)
    else:
        raise Exception(InvalidPathError)

def write_toml(path : str, data : Dict) -> bool:
    """ given the path to a toml file and data stored in a dictionary 
        output the data in the toml format to the file
    """
    try:
        with open(path, "w") as f:
            toml.dump(data, f)
    except:
        raise Exception(InvalidPathError)


def run_cmd(
    cmd : List[str],
) -> int:
    """
    Run the command as a shell command and obtain an identifier.
    The identifier can be used to obtain the shell command status using
    get_cmd_process_status.
    
    Args:
        cmd: List[str]
            A list of string that stores the command 
    
    Return:
        the process id that can be used to identify the process the command 
        runs on 
    """
    process = subprocess.Popen(
        cmd, stdout = subprocess.PIPE, stderr= subprocess.PIPE)
    
    pid = process.pid
    return pid

def get_cmd_status(identifier : int) -> CMD_STATUS:
    """
    Obtain the status of the shell command associated with this identifier
    
    Args: 
        identifier: int 
            the process id of a running process 
    
    Return 
        a string representing the process status 
    """
    try:
        process = psutil.Process(identifier)
        status = process.status()
        match status:
            case "zombie":
                return CMD_STATUS.FINISHED 
            case "running":
                return CMD_STATUS.RUNNING
            case "stopped":
                return CMD_STATUS.RUNNING
            case other:
                return CMD_STATUS.ERROR
    except psutil.NoSuchProcess:
        return CMD_STATUS.NOTFOUND
    