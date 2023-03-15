# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-08-24 11:16:10
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-08-24 11:35:23

import os
import sys

from pathlib import Path
from src import (
    generate_config,
    available_plugins
)

_SUITE_NAME = "gb_hilab_suite"

def get_module_path():
    """Obtain the path of the module"""
    return os.path.dirname(__file__)

def get_config_path():
    return Path("./config.json").absolute()


if __name__ == "__main__":
    print(f"Setting up plugin suite: {_SUITE_NAME}")
    print(f"Available plugins: {available_plugins()}")
    generate_config()
    print(f"Configuration generated at: {get_config_path()}")
