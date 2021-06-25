# Standard library imports
from Src.Components.analyzer.models.plugin_details import PluginDetails
from typing import Any, Dict, Tuple, List
import os
import imp
# Local imports
from .models.config import PluginConfig
from .models.plugin_data import PluginData
from .models.plugin_details import PluginDetails
from .plugin import Plugin
from ..io import IO
from ...utils.manager import ObjectManager

# Third party imports

class PluginLoader:

    def __init__(self) -> None:
        ## Vars
        self.plugin_class_name = "Plugin"
        self.plugin_source_name = "plugin"
        ## Objects
        self.io = IO()
        self.plugins = ObjectManager()

    ################################# MODIFIERS #############################

    def load_plugin_from_directory(self, plugin_dir_path) -> bool:
        return self._load_plugin_directory(plugin_dir_path)

    def load_plugin_from_file(self, plugin_config : PluginConfig,
            plugin_file_path : str) -> bool:
        if not self.io.is_file(plugin_file_path):
            return False
        did_initialize, plugin_object = \
            self._initialize_plugin_object_from_file(plugin_file_path)
        if not did_initialize:
            return False
        plugin_data = self._initialize_plugin_data(plugin_config,plugin_object)
        return self.plugins.add_object(
            plugin_config.plugin_name,plugin_data, True)

    def load_plugin_subdirectories(self, parent_dir_path : str) -> bool:
        if not self.io.is_directory(parent_dir_path):
            return False
        num_loaded = 0
        _, subdirectory_paths = self.io.paths_of_subdirectories(parent_dir_path)
        for dir_path in subdirectory_paths:
            if self.load_plugin_from_directory(dir_path):
                num_loaded += 1
        return num_loaded > 0

    ################################# GETTERS ###############################

    def is_plugin_loaded(self, plugin_name : str) -> bool:
        return self.plugins.is_object(plugin_name)

    def get_loaded_plugin_names(self) -> List[str]:
        return self.plugins.get_object_names()

    def get_plugin(self, plugin_name : str) -> PluginData:
        if not self.plugins.is_object(plugin_name):
            return
        return self.plugins.get_object(plugin_name)

    def get_all_plugins(self) -> Dict[str,PluginData]:
        return self.plugins.get_all_objects()

    def get_plugin_details(self, plugin_name : str) -> PluginDetails:
        if not self.is_plugin_loaded(plugin_name):
            return
        plugin_data : PluginData = self.plugins.get_object(plugin_name)
        return PluginDetails(
            plugin_data.plugin_name,
            plugin_data.plugin_dependencies)

    def get_all_plugin_details(self) -> Dict[str,PluginDetails]:
        details = dict()
        for plugin_name in self.get_loaded_plugin_names():
            details[plugin_name] = self.get_plugin_details(plugin_name)
        return details

    ######################### PRIVATE METHODS ###############################

    def _load_plugin_directory(self, plugin_dir_path : str) -> bool:
        """
        Load plugin objects from a directory.
        The plugin directory must have a plugin.py file with a Plugin class
        and  config.json file.
        """
        if not self.io.is_directory(plugin_dir_path):
            return False
        # Ensure that the correct files are present
        _, plugin_file_paths = self.io.path_of_files_in_directory(
            plugin_dir_path,["py"],False)
        _, config_file_paths = self.io.path_of_files_in_directory(
            plugin_dir_path,["json"],False)
        if len(plugin_file_paths) != 1 or len(config_file_paths) != 1:
            return False
        # Loading the config object
        did_load_config, plugin_config = self._initialize_config_from_file(
            config_file_paths[0])
        if not did_load_config:
            return False
        # Load using the config object
        return self.load_plugin_from_file(plugin_config, plugin_file_paths[0])

    def _initialize_plugin_object_from_file(self, plugin_file_path : str) \
            -> Tuple[bool,Plugin]:
        try:
            module_type = imp.load_source(self.plugin_source_name,plugin_file_path)
            clazz = getattr(module_type,self.plugin_class_name)
            instance = clazz()
            return (True, instance)
        except Exception as e:
            return (False, None)

    def _initialize_config_from_file(self, config_file_path : str) \
            -> Tuple[bool,Plugin]:
        try:
            _, data = self.io.read(config_file_path)
            config = PluginConfig(data["plugin_name"], data["plugin_dependencies"])
            return (True, config)
        except Exception as e:
            return (False, None)

    def _initialize_plugin_data(self, plugin_config : PluginConfig,
            plugin_object : Plugin) -> PluginData:
        return PluginData(
            plugin_object, plugin_config.plugin_name,
            plugin_config.plugin_dependencies,
            len(plugin_config.plugin_dependencies))
