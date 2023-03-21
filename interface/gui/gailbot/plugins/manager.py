# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 13:22:01
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-16 13:10:15

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
    delete, 
    get_name, 
    is_directory
)


logger = makelogger("plugin_manager")
class DuplicatePlugin(Exception):
    def __str__(self) -> str:
        return "ERROR: loading existing plugin" 
class PluginManager:
    """
    Manage multiple plugins suites that can be registered, including
    storing the plugin files, parsing the config files, and instantiating
    plugin objects from files.
    """
    def __init__(
        self,
        workspace: str, 
        plugin_sources : List[str] = [],
        load_existing : bool = True,
        over_write: bool = True
    ):
        self.workspace = workspace
        self._init_workspace()
        """ check if the plugin has been installed  """
        self.loaders: List[PluginLoader] = [
            PluginURLLoader(self.download_dir, self.suites_dir),
            PluginDirectoryLoader(self.suites_dir)
        ]
        
        source_names = {get_name(path) for path in plugin_sources}
        subdirs = subdirs_in_dir(self.suites_dir, recursive=False)
       
        for subdir in subdirs: 
            if get_name(subdir[:-1]) in source_names:
                logger.info("duplicate found")
                if over_write or (not load_existing): 
                    delete(subdir)
                else: 
                    raise DuplicatePlugin(f"plugin {get_name(subdir)} already exist") 
        
        if load_existing:
            # get a list of paths to existing suite 
            subdirs = subdirs_in_dir(self.suites_dir, recursive=False)
            logger.info(f"all sub directories are {subdirs}")
            subdirs = [dir[:-1] for dir in subdirs] 
            
            plugin_sources.extend(subdirs)

        for plugin_source in plugin_sources:
            if not self.register_suite(plugin_source):
                logger.error(f"{get_name(plugin_source)} cannot be registered")
    
    def get_all_suites_name(self) -> List[str]:
        return set(self.suites.keys())

    def is_suite(self, suite_name : str) -> bool:
        return suite_name in self.suites

    def reset_workspace(self) -> bool:
        """
        Reset all the plugins that currently exist.
        They will be permanently deleted and will have to be re-added.
        """
        make_dir(self.workspace,overwrite=True)

    def register_suite(
        self,
        plugin_source : str
    ) -> Union[str, bool]:
        """
        Register a plugin suite from the given source, which can be
        a plugin directory, a url, a conf file, or a dictionary configuration.
        """
        try:
            for loader in self.loaders:
                suite = loader.load(plugin_source) 
                if suite and isinstance(suite, PluginSuite):
                    self.suites[suite.name] = suite
                    return suite.name
            return False
        except Exception as e:
            logger.error(e, exc_info=e)
            return False
        
    def get_suite(
        self,
        suite_name : str
    ) -> PluginSuite:
        if not self.is_suite(suite_name):
            logger.error(f"Suite does not exist {suite_name}")
            return None
        return self.suites[suite_name]

    def _init_workspace(self):
        """
        Init workspace and load plugins from the specified sources.
        """         
        self.suites_dir = f"{self.workspace}/suites"
        self.download_dir = f"{self.workspace}/downloads"
        sys.path.append(self.suites_dir)
        self.suites = dict()
        
        # Make the directory
        make_dir(self.workspace,overwrite=False)
        make_dir(self.suites_dir,overwrite=False)
        make_dir(self.download_dir,overwrite=True)
    
    def delete_suite(self, name:str):
        if self.is_suite(name):
            delete(os.path.join(self.suites_dir, name))
            del self.suites[name]
            return True 
        else:
            return False
                
    def get_suite_path(self, name:str) -> str:
        """ given a name of the suite, return the suite path that is internally 
            managed by the suite manager
        """
        if self.is_suite(name):
            path = os.path.join(self.suites_dir, name)
            if is_directory(path):
                return path
            else:
                del self.suite_names[name]
                return "WARNING: suite source has been deleted"
        else:
            return "suite not found"     
    
    