# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 13:22:01
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-16 13:10:15
from dataclasses import dataclass
import sys
import os
from typing import  List, Union, Dict
import validators
from .suite import PluginSuite
from .loader import (
    PluginURLLoader,  
    PluginDirectoryLoader,
    PluginLoader)
from gailbot.core.utils.logger import makelogger
from gailbot.configs import PLUGIN_CONFIG
from gailbot.core.utils.general import (
    make_dir,
    subdirs_in_dir,
    delete, 
    get_name, 
    is_directory,
    filepaths_in_dir,
    paths_in_dir
)

logger = makelogger("plugin_manager")

@dataclass 
class ERROR: 
    INVALID_URL    = "The given url is not supported by gailbot"
    MISSING_CONFIG = "The plugin suite is missing config.toml that specifies the plugins dependency"
    MISSING_DOC    = "The plugin suite is missing a DOCUMENT.md file"
    MODULE_ERROR   = "Fail to load import plugin module"
    INVALID_INPUT  = "The plugin suite source can only be URL, a valid Amazon S3 Bucket name, or path to directory"
    
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
        load_existing : bool = True,
        over_write: bool = True
    ):
        """
        Args:
        workspace (str) : the path to plugin workspace 
        plugin_sources:   a list of paths to plugin sources
        loading_existing: if true, load the existing plugin from plugin workspace
        over_write: if true, overwrite the existing plugin if plugins_sources 
                    contain plugin that has already been saved in workspace
        """ 

        self.workspace = workspace
        logger.info(f"get workspace {self.workspace}")
        self._init_workspace()
      
        self.loaders: List[PluginLoader] = [
            PluginURLLoader(self.download_dir, self.suites_dir),
            PluginDirectoryLoader(self.suites_dir)
        ]
         
        if load_existing:
            subdirs = subdirs_in_dir(self.suites_dir, recursive=False)
            for plugin_source in subdirs:
                if not self.register_suite(plugin_source):
                    logger.error(f"{get_name(plugin_source)} cannot be registered")
        try:
            self.register_suite(PLUGIN_CONFIG.HILAB_BUCKET)
        except Exception as e:
            logger.error(e, exc_info=e)
        
    def get_all_suites_name(self) -> List[str]:
        """ return a list of available plugin suite names  """
        return set(self.suites.keys())

    def is_suite(self, suite_name : str) -> bool:
        """ check if suite name is an available plugin suite """
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
    ) -> Union[List[str], str]:
        """
        Register a plugin suite from the given source, which can be
        a plugin directory, a url, a conf file, or a dictionary configuration.
        """
        registered = []
        try:
            for loader in self.loaders:
                suites = loader.load(plugin_source) 
                if suites and isinstance(suites, list):
                    for suite in suites: 
                        if isinstance(suite, PluginSuite):
                            self.suites[suite.name] = suite
                            registered.append(suite.name)
                    return registered
            return self.report_registration_err(plugin_source)
        except Exception as e:
            logger.error(e, exc_info=e)
            return self.report_registration_err(plugin_source)
        
    def get_suite(
        self,
        suite_name : str
    ) -> PluginSuite:
        """ Given a suite name, return the plugin suite object

        Args:
            suite_name (str): the name that identifies the plugin suite

        Returns:
            PluginSuite: the plugin suite object identified by suite name
        """
        if not self.is_suite(suite_name):
            logger.error(f"Suite does not exist {suite_name}")
            return None
        return self.suites[suite_name]

    def get_suite_metadata(self, suite_name:str) -> Dict[str, str]:
        if not self.is_suite(suite_name):
            logger.error(f"Suite does not exist {suite_name}")
            return None
        return self.suites[suite_name].get_meta_data()
    
    def get_suite_dependency_graph(self, suite_name:str) -> Dict[str, List[str]]:
        if not self.is_suite(suite_name):
            logger.error(f"Suite does not exist {suite_name}")
            return None
        return self.suites[suite_name].dependency_graph()
    
    def get_suite_documentation_path(self, suite_name) -> str:
        if not self.is_suite(suite_name):
            logger.error(f"Suite does not exist {suite_name}")
            return None
        return self.suites[suite_name].document_path
   
    def is_official_suite(self, suite_name) -> bool:
        if not self.is_suite(suite_name):
            logger.error(f"Suite does not exist {suite_name}")
            return None
        return self.suites[suite_name].is_official
      
    def _init_workspace(self):
        """
        Init workspace and load plugins from the specified sources.
        """         
        self.suites_dir = f"{self.workspace}/suites"
        self.download_dir = f"{self.workspace}/downloads"
        sys.path.append(self.suites_dir)
        self.suites: Dict [str, PluginSuite] = dict()
        
        # Make the directory
        make_dir(self.workspace, overwrite=False)
        make_dir(self.suites_dir,overwrite=False)
        make_dir(self.download_dir,overwrite=True)
    
    def delete_suite(self, name:str):
        """ 
        given a suite name, delete the plugin suite
        """
        try:
            if self.is_suite(name):
                delete(os.path.join(self.suites_dir, name))
                del self.suites[name]
                return True 
            else:
                return False
        except Exception as e:
            logger.error(e, exc_info=e)
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
                del self.suites[name]
                return None
        else:
            return None
    
    # TODO: improve this function to generate more specific error message
    def report_registration_err(self, suite:str) -> str:
        if validators.url(suite):
            if not PluginURLLoader.is_valid_url(suite):
                return ERROR.INVALID_URL
            else:
                return ERROR.MODULE_ERROR 
        elif is_directory(suite):
            tomls = filepaths_in_dir(suite, ["toml"])
            if len(tomls) == 0 or not tomls:
                return ERROR.MISSING_CONFIG
                
            mds = filepaths_in_dir(suite, ["md"])
            if len(mds) == 0 or not mds:
                return ERROR.MISSING_DOC
                
            return ERROR.MODULE_ERROR 
        else:
            return ERROR.INVALID_INPUT
        
         