# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 13:50:28
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-12 14:36:19

import sys
import os
from typing import List, Dict
from dataclasses import dataclass
from types import SimpleNamespace
from dotwiz import DotWiz
from gailbot.core.utils.general import (
    make_dir
)



@dataclass
class DataFile:
    path : str

class Settings:
    """
    Simply gets a dictionary and converts it into a simple namespace that
    can be accessed via dot notation.
    TODO: Potentially validate the data structure
    """
    def __init__(
        self,
        name : str,
        data : Dict,
        save_path : str
    ):
        self.name = name
        self.data = DotWiz(data)
        self.save_path = save_path

    def to_dict(self) -> Dict:
        return self.data.to_dict()

class Source:

    def __init__(
        self,
        identifier : str,
        workspace_dir : str,
        data_files : List[DataFile],
        settings_profile : Settings = None
    ):
        """
        Create the workspace for the source in the given workspace,
        initialize the datafiles
        """
        self.identifier = identifier
        self.workspace_dir = workspace_dir
        self.data_files = data_files
        self.settings_profile = settings_profile
        self.workspace = workspace_dir
        make_dir(self.workspace, overwrite=True)

    @property
    def workspace(self):
        """Path to the workspace for this source"""
        return self.workspace

    @property
    def configured(self):
        return self.settings_profile != None

    def to_dict(self) -> Dict:
        pass











