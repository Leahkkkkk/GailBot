# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 13:22:01
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-12 14:59:54

import sys
import os
from typing import Dict, List, Any
from dataclasses import dataclass
from .plugin import Plugin
from .suite import PluginSuite

from gailbot.core.utils.general import (
    make_dir,
    paths_in_dir,
    get_name,
    move,
    copy
)
from gailbot.core.utils.download import download_from_urls

@dataclass
class PluginDetails:
    pass

class PluginManager:
    """
    Manage multiple plugins suites that can br registered, including
    storing the plugin files, parsing the config files, and instantiating
    plugin objects from files.
    """

    def __init__(
        self,
        workspace_dir : str,
        suite_urls : List[str] = None
    ):
        self.workspace_dir = workspace_dir
        self.suites_dir = f"{workspace_dir}/suites"
        self.download_dir = f"{workspace_dir}/downloads"
        self.suites = dict()

        # Make the directory
        make_dir(workspace_dir,overwrite=False)
        make_dir(self.suites_dir,overwrite=False)
        make_dir(self.download_dir,overwrite=True)
        # Load any suites that may already exist

        # Download if required
        if suite_urls != None:
            for url in suite_urls:
                self._load_suite_from_url(url)

    def is_suite(self, suite_name : str) -> bool:
        return suite_name in self.suites

    def reset_workspace(self) -> bool:
        """Reset all the plugins that currently exist"""
        make_dir(self.workspace_dir,overwrite=True)

    def register_suite(
        self,
        suite_dir_or_url : str
    ) -> Dict:
        """
        Register a plugin suite from the given path or url
        """
        if os.path.isdir(suite_dir_or_url):
            suite = self._load_suite_from_disk(suite_dir_or_url)
        else:
            suite = self._load_suite_from_url(suite_dir_or_url)

        return suite.details() if suite != None else suite

    def get_suite(
        self,
        suite_name : str
    ) -> PluginSuite:
        if self.is_suite(suite_name):
            raise Exception(
                f"Suite does not exist {suite_name}"
            )
        return self.suites[suite_name]

    def _load_suite_from_url(self, url : str) -> bool:
        # Download from url
        suite_dir_path = download_from_urls(
            urls=[url],
            download_dir=self.download_dir,
            unzip=True
        )[0]
        # Move to the suites dir.
        suite_dir_path = move(suite_dir_path,self.suites_dir)
        return self._load_suite_from_disk(suite_dir_path)

    def _load_suite_from_disk(self, suite_dir_path : str) -> bool:
        """
        Load a suite from the dir. The name of the dir counts as the name
        of the suite.
        """

        # Load the first toml file in dir.
        # TODO: Might want to name this something specific
        # Move to the plugins dir
        suite_dir_path = copy(suite_dir_path,self.suites_dir)
        suite = PluginSuite(suite_dir_path)
        if not suite.name in self.suites:
            self.suites[suite.name] = suite
            return True
        return False





