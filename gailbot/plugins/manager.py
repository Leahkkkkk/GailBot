# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 13:22:01
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-16 13:10:15
""" TODO:  """
import sys
import os
from typing import Dict, List, Any
from dataclasses import dataclass
from .plugin import Plugin
from .suite import PluginSuite

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


class PluginLoader:

    def load(self, *args, **kwargs) -> PluginSuite:
        raise NotImplementedError()

class PluginURLLoader(PluginLoader):

    def __init__(
        self,
        download_dir : str,
        suites_dir : str
    ):
        self.download_dir = download_dir
        self.suites_dir = suites_dir
        self.dir_loader = PluginDirectoryLoader(suites_dir)

    def load(self, url : str) -> PluginSuite:
         # Download from url
        suite_dir_path = download_from_urls(
            urls=[url],
            download_dir=self.download_dir,
            unzip=True
        )[0]
        # Move to the suites dir.
        suite_dir_path = move(suite_dir_path,self.suites_dir)
        return self.dir_loader.load(suite_dir_path)

class PluginDirectoryLoader(PluginLoader):

    def __init__(
        self,
        suites_dir : str
    ):
        self.suites_dir = suites_dir
        self.toml_loader = PluginTOMLLoader()

    def load(self, suite_dir_path : str) -> PluginSuite:

        if not os.path.isdir(suite_dir_path):
            return
        # Load the first toml file in dir.
        # TODO: Might want to name this something specific
        # Move to the plugins dir
        tgt_path = f"{self.suites_dir}/{get_name(suite_dir_path)}"
        if not is_directory(tgt_path):
            suite_dir_path = copy(suite_dir_path,tgt_path)
        # Suite should only load from dict config
        conf = filepaths_in_dir(suite_dir_path,["toml"])[0]
        return self.toml_loader.load(conf)


class PluginTOMLLoader(PluginLoader):

    def __init__(self):
        self.dict_config_loader = PluginDictLoader()

    def load(self, conf_path : str) -> PluginSuite:
        if not os.path.isfile(conf_path) and \
                not get_extension(conf_path) == "toml":
            return
        dict_conf = read_toml(conf_path)
        # Adding the absolute path
        print(conf_path)
        dict_conf.update({
            "path" : get_parent_path(conf_path)
        })
        return self.dict_config_loader.load(dict_conf)

class PluginDictLoader(PluginLoader):

    def load(self, dict_conf : Dict) -> PluginSuite:
        # TODO: THis is where the dict conf should be parsed
        # The suite itself should dynamically load the classes.
        if not type(dict_conf) == dict:
            return
        suite = PluginSuite(dict_conf)
        if suite.is_ready:
            return suite


class PluginManager:
    """
    Manage multiple plugins suites that can br registered, including
    storing the plugin files, parsing the config files, and instantiating
    plugin objects from files.
    """

    def __init__(
        self,
        workspace_dir : str,
        plugin_sources : List[str] = [],
        load_existing : bool = True
    ):
        """
        Init workspace and load plugins from the specified sources.
        """
        self.workspace_dir = workspace_dir
        self.suites_dir = f"{workspace_dir}/suites"
        self.download_dir = f"{workspace_dir}/downloads"
        self.suites = dict()
        """ TODO: test this - load different types of plugin source file """
        self.loaders = [
            PluginDirectoryLoader(self.suites_dir),
            PluginTOMLLoader(),
            PluginDictLoader(),
            PluginURLLoader(self.download_dir, self.suites_dir),
        ]

        # Make the directory
        make_dir(workspace_dir,overwrite=False)
        make_dir(self.suites_dir,overwrite=False)
        make_dir(self.download_dir,overwrite=True)
        
        """ check if the plugin has been installed  """
        if load_existing:
            # TODO:  Load any suites that may already exist
            subdirs = subdirs_in_dir(self.suites_dir)
            # Treat each subdir as a plugin that can be loaded from dir.
            plugin_sources.extend(subdirs)

        # TODO: Load plugins from the specified sources.
        for plugin_source in plugin_sources:
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
        for loader in self.loaders:
            suite = loader.load(plugin_source)
            if isinstance(suite, PluginSuite):
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
        pass 





