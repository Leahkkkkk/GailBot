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
# Local imports
# Third party imports
from copy import deepcopy
import subprocess


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

def delete(path : str) -> None:
    """ given a path, delete the file """
    if is_file(path):
        Path(path).unlink(missing_ok=True)
    elif is_directory(path):
        shutil.rmtree(path)
    else:
        return False
    
    
def is_file(file_path: str) -> bool:
    """
    Determine if the given path is a file.
    """
    try:
        return Path(file_path).is_file()
    except:
        return False


def is_path(source:str):
    return is_file(source) or is_directory(source)


def is_directory(dir_path: str) -> bool:
    """
    Determine if the given path is a directory.
    """
    try:
        return Path(dir_path).is_dir()
    except:
        return False