# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 16:28:03
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-16 14:39:45
from enum import Enum 
from typing import List, Dict
import psutil
import os
import glob
import shutil
import itertools
from pathlib import Path
import subprocess
from gailbot.core.utils.logger import makelogger

import json
import yaml
import toml
import csv

logger = makelogger("general")

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
    except Exception as e:
        logger.error(dir_path, exc_info =e)
        return False 

def is_file(file_path: str) -> bool:
    """
    Determine if the given path is a file.
    """
    try:
        return Path(file_path).is_file()
    except Exception as e:
        logger.error(file_path, exc_info =e)
        return False

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
    except Exception as e:
        logger.error(e)
        return False


def is_path(source:str):
    return is_file(source) or is_directory(source)

    
def paths_in_dir(
    path: str,
    extensions: List[str] = ["*"],
    recursive: bool = False,
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
        logger.error("not a valid directory")
        return False
    try: 
        if only_dirs:
            return glob.glob(f"{path}/*/",recursive=recursive)
        else:
            return list(itertools.chain(
                *[glob.glob(f"{path}/*.{ext}",recursive=recursive) for \
                    ext in extensions]
            ))
    except Exception as e:
        logger.error(e)
        return False

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
    except Exception as e:
        logger.error(e) 
        return False
    
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
    except Exception as e:
        logger.error(e)
        return False

def num_subdirs(dir_path : str, recursive : bool = False) -> int:
    """Get the number of subdirectory in the dir_path"""
    try:
        return len(subdirs_in_dir(dir_path,recursive))
    except Exception as e:
        logger.error(e)
        return False
        

def get_name(path : str) -> str:
    """given the path return the name of file or dir without extension"""
    try: 
        dir_path, file_name = os.path.split(path)
        if file_name:
            return os.path.splitext(os.path.basename(path))[0]
        else:
            return os.path.basename(dir_path)
    except Exception as e:
        logger.error(e)
        return False
        

def get_extension(path : str) -> str:
    """ given the path to the file, return the extension of the file """
    try: 
        return os.path.splitext(os.path.basename(path))[1][1:]
    except Exception as e:
        logger.error(e)
        return False


def get_parent_path(path : str) -> str:
    """ given the path to the file, returns the path to the file's 
        parent directory"""
    try:
        return str(Path(path).parent.absolute())
    except Exception as e:
        logger.error(e)
        return False

def get_size(path : str) -> bytes:
    """given the path to the file, return the file size"""
    try:
        if is_file(path):
            return os.path.getsize(path)
        else:
            return sum([
                os.path.getsize(p) for p in filepaths_in_dir(path,recursive=True)
            ])
    except Exception as e:
        logger.error(e)
        return False 

def make_dir(path : str, overwrite : bool = False):
    """ given the path, create a directory """
    logger.info(f"making directory is called on making the path {path}")
    try:
        if is_directory(path) and overwrite:
            delete(path)
        os.makedirs(path, exist_ok=True)
    except Exception as e:
        logger.error(e)
        return False 
        

def move(src_path : str, tgt_path : str) -> str:
    """ move the file from the source path to the target path """
    try:
        return shutil.move(src_path, tgt_path)
    except Exception as e:
        logger.error(e)
        return False 
        
        
def copy(src_path, tgt_path : str) -> str:
    """ copy the file from the source path to the target path """
    try:
        if is_file(src_path):
            return shutil.copy(src_path, tgt_path)
        elif is_directory(src_path):
            return shutil.copytree(src_path, tgt_path,dirs_exist_ok=True)
        else:
            logger.error("not a valid file path")
    except Exception as e:
        logger.error(e)
        return False
    

def rename(src_path, new_name : str) -> str:
    """ rename the file in the source path to the new name """
    try:
        return str(Path(src_path).rename(new_name).resolve())
    except Exception as e:
        logger.error(e)
        raise FileExistsError
    
def delete(path : str) -> None:
    """ given a path, delete the file """
    try: 
        if is_file(path):
            Path(path).unlink(missing_ok=True)
        elif is_directory(path):
            shutil.rmtree(path)
        else:
            logger.error("not a valid path")
            return False
    except Exception as e:
        logger.error(e)
        return False

def read_json(path : str) -> Dict:
    """ given a path, read the json data stored in the file, return the 
        a dictionary that stores the json data 
    """
    if is_file(path):
        with open(path, 'r') as f:
            return json.load(f)
    else:
        raise FileExistsError

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
        raise FileExistsError

def write_txt(path : str, data : List,  overwrite : bool = True) -> bool:
    """ given the path to a file, and a list of data, output the list 
        data to the file
    """
    mode = 'w+' if overwrite else "a"
    data = [s + "\n" for s in data]
    try:
        with open(path, mode) as f:
                f.writelines(data)
    except Exception as e:
        logger.error
        raise FileExistsError
    
    
def read_yaml(path : str) -> Dict:
    """ given a path to a yaml file, return a dictionary 
        representation of the data stored in the yaml file 
    """
    logger.info(f"path is {path}")
    # with open(path, "r") as f:
    #     text = f.read()
    #     logger.info(f"all the text in the file is {text}")
        
    if is_file(path):
        try:
            with open(path, 'r') as f:
                data = yaml.safe_load(f)  # NOTE: added the required parameter Loader
                # Data loaded must be a dictionary
                if not data:
                    logger.warn(f"safe load data failed, try unsafe load")
                    data = yaml.unsafe_load(path)
                if not type(data) == dict:
                    logger.error(f"the data is not a valid dictionary: {data}, the file path is {path}")
                    raise Exception
                return data
        except Exception as e:
            logger.error(e, exc_info=e)
    else:
        logger.error("not a valid yaml file")
        raise FileExistsError
 

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
    except Exception as e:
        logger.error(e)
        raise FileExistsError

def read_toml(path : str) -> Dict:
    """ given the path to a to toml file, return a dictionary 
        representation of the data stored in the toml file
    """
    if is_file(path):
        return toml.load(path)
    else:
        logger.error("not a valid toml file")
        raise FileExistsError

def write_toml(path : str, data : Dict) -> bool:
    """ given the path to a toml file and data stored in a dictionary 
        output the data in the toml format to the file
    """
    try:
        with open(path, "w+") as f:
            toml.dump(data, f)
    except Exception as e:
        logger.error(e)
        raise FileExistsError

def write_csv(path: str, data: List[Dict[str, str]]):
    if not data or len(data) == 0:
        with open(path, mode="w+", newline="") as file:
            pass 
        return
    fields = list(data[0].keys())
    # Write the data to the CSV file
    with open(path, mode='w+', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def read_csv(path:str) -> List[Dict[str, str]]:
    data = []
    with open(path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data


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
    
    
def copy_dir_files(src_folder, dest_folder):
    """ copy files from src_folder to dest_folder recursively

    Args:
        src_folder (str): the path to the source folder
        dest_folder (str): the path to the destination folder
    """
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    # Walk through the source directory tree
    for root, dirs, files in os.walk(src_folder):
        # Create the corresponding subdirectories in the destination folder
        dest_root = root.replace(src_folder, dest_folder)
        for dir_name in dirs:
            dest_dir = os.path.join(dest_root, dir_name)
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)

        # Copy the files to the destination folder
        for filename in files:
            src_path = os.path.join(root, filename)
            dest_path = os.path.join(dest_root, filename)
            shutil.copy2(src_path, dest_path)