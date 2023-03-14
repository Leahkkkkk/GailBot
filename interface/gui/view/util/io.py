from enum import Enum 
import sys
import psutil
from typing import Any, Callable, Tuple, List, Dict
import os
import glob
import json 
import yaml
import toml
import csv
import shutil
import itertools
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
# Local imports
# Third party imports
import logging 
from copy import deepcopy
import subprocess

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
        logging.error("not a valid directory")
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
        logging.error(e)
        return False

def get_name(path : str) -> str:
    """given the path return the name of file or dir without extension"""
    try: 
        dir_path, file_name = os.path.split(path)
        if file_name:
            return os.path.splitext(os.path.basename(path))[0]
        else:
            return os.path.basename(dir_path)
    except:
        return False
    
    
def is_file(file_path: str) -> bool:
    """
    Determine if the given path is a file.
    """
    try:
        return Path(file_path).is_file()
    except:
        return False


def is_directory(dir_path: str) -> bool:
    """
    Determine if the given path is a directory.
    """
    try:
        return Path(dir_path).is_dir()
    except:
        return False

def zip_file(source: str, tgt: str, extension: str) -> bool:
    """ zip the file from source and output a zipped file to tgt"""
    try:
        zip_file = ZipFile(tgt, 'w', ZIP_DEFLATED)
        for root, dirs, files in os.walk(source):
            for file in files:
                # Check if the file is a log file
                if file.endswith(extension):
                    # Get the full path of the file
                    file_path = os.path.join(root, file)
                    # Add the file to the zip_file with the same directory structure
                    zip_file.write(file_path, arcname = os.path.join(
                                                        os.path.basename(os.path.dirname(file_path)),
                                                        os.path.basename(file_path)))
    except Exception as e:
        logging.error(e)
        return False
             
        
def copy(src_path, tgt_path : str) -> str:
    """ copy the file from the source path to the target path """
    try:
        if is_file(src_path):
            return shutil.copy(src_path, tgt_path)
        elif is_directory(src_path):
            return shutil.copytree(src_path, tgt_path,dirs_exist_ok=True)
        else:
            logging.error("not a valid file path")
    except Exception as e:
        logging.error(e)
        return False
    
def delete(path : str) -> None:
    """ given a path, delete the file """
    try: 
        if is_file(path):
            Path(path).unlink(missing_ok=True)
        elif is_directory(path):
            shutil.rmtree(path)
        else:
            logging.error("not a valid path")
            return False
    except Exception as e:
        logging.error(e)
        return False