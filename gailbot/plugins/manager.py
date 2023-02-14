# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 13:22:01
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-16 13:10:15
#
# TODO: 
#       rename the suite directory to be the same as the suite name 
# .     rename suite

import sys
import os
from typing import Dict, List, Union
from .suite import PluginSuite
from.loader import (
    PluginURLLoader,  
    PluginDirectoryLoader,
    PluginLoader)
from gailbot.core.utils.logger import makelogger
from gailbot.core.utils.general import (
    make_dir,
    subdirs_in_dir,
    delete
)
from gailbot.configs import top_level_config_loader 
from pprint import pprint

TOP_LEVEL = top_level_config_loader()
logger = makelogger("plugin_manager")
class PluginManager:
    """
    Manage multiple plugins suites that can be registered, including
    storing the plugin files, parsing the config files, and instantiating
    plugin objects from files.
    """
    def __init__(
        self,
        plugin_sources : List[str] = [],
        load_existing : bool = True,
        overwrite : bool = True
    ):
        self._init_workspace()
        """ check if the plugin has been installed  """
        self.overwrite = overwrite
        self.loaders: List[PluginLoader] = [
            PluginURLLoader(self.download_dir, self.suites_dir),
            PluginDirectoryLoader(self.suites_dir)
        ]
        
        if load_existing:
            # get a list of paths to existing suite 
            subdirs = subdirs_in_dir(self.suites_dir)
            plugin_sources.extend(subdirs)

        for plugin_source in plugin_sources:
            logger.info(f"get plugin source {plugin_source}")
            self.register_suite(plugin_source)
    
    @property
    def suite_names(self) -> List[str]:
        return set(self.suites.keys())

    def is_suite(self, suite_name : str) -> bool:
        return suite_name in self.suites

    def reset_workspace(self) -> bool:
        """
        Reset all the plugins that currently exist.
        They will be permanently deleted and will have to be re-added.
        """
        make_dir(self.workspace_dir,overwrite=True)

    def register_suite(
        self,
        plugin_source : str
    ) -> Dict:
        """
        Register a plugin suite from the given source, which can be
        a plugin directory, a url, a conf file, or a dictionary configuration.
        """
        logger.info("register plugin")
        for loader in self.loaders:
            suite = loader.load(plugin_source, self.overwrite)
            if suite and isinstance(suite, PluginSuite):
                logger.info("get suite")
                self.suites[suite.name] = suite
                return suite.dependency_graph()

    def get_suite(
        self,
        suite_name : str
    ) -> PluginSuite:
        if not self.is_suite(suite_name):
            raise Exception(
                f"Suite does not exist {suite_name}"
            )
        return self.suites[suite_name]

    def _init_workspace(self):
        """
        Init workspace and load plugins from the specified sources.
        """        
        self.workspace_dir = os.path.join(
            TOP_LEVEL.root, TOP_LEVEL.workspace.plugin_workspace)
        
        self.suites_dir = f"{self.workspace_dir}/suites"
        self.download_dir = f"{self.workspace_dir}/downloads"
        sys.path.append(self.suites_dir)
        self.suites = dict()
        
        # Make the directory
        make_dir(self.workspace_dir,overwrite=False)
        make_dir(self.suites_dir,overwrite=False)
        make_dir(self.download_dir,overwrite=True)

    def rename_suite(self):
        """ NOTE: this will cause a problem when trying to import the suite """
        raise NotImplementedError

    def delete_suite(self, name:str):
        if self.is_suite(name):
            delete(os.path.join(self.suites_dir, name))
            del self.suites[name]
            return True 
        else:
            return False

    def get_suite_path(self, name:str) -> str:
        """  """
        if self.is_suite(name):
            return os.path.join(self.suites_dir, name)
        else:
            return "suite not found"     