# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 13:22:01
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-16 13:10:15
import sys
import os
import urllib.parse
from typing import Dict, List, Union
from .suite import PluginSuite
from gailbot.core.utils.logger import makelogger
from gailbot.core.utils.general import (
    make_dir,
    subdirs_in_dir,
    filepaths_in_dir,
    get_name,
    get_extension,
    move,
    copy,
    read_toml,
    get_parent_path,
    is_directory
)
from gailbot.core.utils.download import download_from_urls
from gailbot.configs import top_level_config_loader 
from pprint import pprint

TOP_LEVEL = top_level_config_loader()
logger = makelogger("plugin_manager")
class PluginLoader:
    """ base class for plugin loader """
    def load(self, *args, **kwargs) -> PluginSuite:
        raise NotImplementedError()

class PluginURLLoader(PluginLoader):
    """ load plugin from an url source  """
    def __init__(
        self,
        download_dir : str,
        suites_dir : str
    ):
        """ initialize the plugin loader

        Args:
            download_dir (str): path to where the plugin suite will be downloaded 
            suites_dir (str): path to where the plugin will be stored after 
                              download
        """
        self.download_dir = download_dir
        self.suites_dir = suites_dir
        self.dir_loader = PluginDirectoryLoader(suites_dir)

    def load(self, url : str, suites_directory : str) -> PluginSuite:
        """ download the plugin from a given url and stored a copy of the 
            plugins in the suites directory 

        Args:
            url (str): url for downloading the suite 
            suites_directory  (str): path to where a copy of the plugin suite 
                                    will be store 

        Returns:
            PluginSuite: return a PluginSuite object that stores the loaded suite
        """
        # check if the type is valid
        if not type(url) == str: 
            return False
        result = urllib.parse.urlparse(url)
        if not all([result.scheme, result.netloc]):
            return False
        
        download_path = download_from_urls(
            urls=[url],
            download_dir=self.download_dir,
            unzip=True
        )[0]
        
        # get the suite name from the toml file
        for dirpath, dirnames, filenames in os.walk(download_path):
            for file in filenames:
                if get_extension(file) == "toml":
                    suite_name = read_toml(os.path.join(dirpath, file))["suite_name"]
                    break
        
        # get the suite directory 
        for dirpath, dirnames, filename in os.walk(download_path):
            if suite_name in dirnames:
                suite_path = os.path.join(dirpath, suite_name)
                logger.info(f"the directory path is {suite_path}")
                break
            
        # Move to the suites dir.
        return self.dir_loader.load(suite_path, suites_directory)

class PluginDirectoryLoader(PluginLoader):
    """ load the plugin suite from a directory that contains all source 
        script implementing the plugins, and a toml file that stores 
        configuration information to load the plugin     
    """
    def __init__(
        self,
        suites_dir : str, 
    ):
        """ initialize a plugin directory loader

        Args:
            suites_dir (str): the path to the directory that stores all the 
                              copies of plugins will be stored and managed 
                              by plugin manager 
        """
        self.suites_dir = suites_dir
        self.toml_loader = PluginTOMLLoader()

    def load(self, suite_dir_path: str, suites_directory : str = None )  \
        -> Union [PluginSuite, bool]:
        """ load the plugin from a directory 

        Args:
            suite_dir_path (str): path to the source directory that contains 
                                  the entire plugin suite 
        Returns:
            return a PluginSuite object that stores the loaded suite
            if the plugin can be successfully loaded, return false otherwise
                         
        """
        if (not type(suite_dir_path) == str) \
           or (not is_directory(suite_dir_path)):
            # check for invalid input 
            return False
        
        tgt_path = f"{self.suites_dir}/{get_name(suite_dir_path)}"
        if not is_directory(tgt_path):
            suite_dir_path = copy(suite_dir_path, tgt_path)
        # Suite should only load from dict config
        conf = filepaths_in_dir(suite_dir_path,["toml"])[0]
        return self.toml_loader.load(conf, self.suites_dir )

class PluginTOMLLoader(PluginLoader):
    """  import all modules in the plugin, all plugin sources and dependencies 
         are described in a configuration file in toml format 
    """
    def __init__(self):
        self.dict_config_loader = PluginDictLoader()

    def load(self, conf_path : str, suites_directory : str) -> PluginSuite:
        """  given the path to configuration file of one plugin suite, and 
             the suites directory that stores all plugin suites , 
             import the plugin suite described in the configuration file 

        Args:
            conf_path (str): a path to the configuration file
            suites_directory (str): a path to the directory that contain  
                                    all plugin suites

        Returns:
            PluginSuite: 
            return a PluginSuite object that stores the loaded suite
            if the plugin can be successfully loaded, return false otherwise 
        """
        if not type(conf_path) == str :
            return
        if (not os.path.isfile(conf_path)) or \
                (not get_extension(conf_path) == "toml"):
            return
        dict_conf = read_toml(conf_path)
        # Adding the absolute path
        print(conf_path)
        dict_conf.update({
            "path" : get_parent_path(conf_path)
        })
        return self.dict_config_loader.load(dict_conf, suites_directory )
class PluginDictLoader(PluginLoader):
    """ load a plugin suite from a dictionary that contains the configuration 
        of all plugin dependencies and sources 
    """
    def load(self, dict_conf : Dict, suites_directory : str) -> PluginSuite:
        if not type(dict_conf) == dict:
            return
        suite = PluginSuite(dict_conf, suites_directory)
        if suite.is_ready:
            return suite


class PluginManager:
    """
    Manage multiple plugins suites that can be registered, including
    storing the plugin files, parsing the config files, and instantiating
    plugin objects from files.
    """
    def __init__(
        self,
        workspace_dir : str, 
        plugin_sources : List[str] = [],
        load_existing : bool = True
    ):
        self._init_workspace()
        """ check if the plugin has been installed  """
        
        self.loaders = [
            PluginURLLoader(self.download_dir, self.suites_dir),
            PluginDirectoryLoader(self.suites_dir),
            PluginTOMLLoader(),
            PluginDictLoader(),
        ]
        
        if load_existing:
            # get a list of paths to existing suite 
            subdirs = subdirs_in_dir(self.suites_dir)
            plugin_sources.extend(subdirs)

        for plugin_source in plugin_sources:
            logger.info(f"get plugin source {plugin_source}")
            self.register_suite(plugin_source)
    
    def suite_names(self) -> List[str]:
        return list(self.suites.keys())

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
            suite = loader.load(plugin_source, self.suites_dir)
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

    def delete_suite(self, suite_name:str):
        """ TODO:  """
        pass 

        
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




