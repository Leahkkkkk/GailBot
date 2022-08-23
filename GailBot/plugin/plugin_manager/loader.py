# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-02 13:13:08
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-05-03 12:25:58
# Standard library imports
from typing import Any, List, Dict
import imp
# Local imports
from .config import PluginConfig
from .plugin_source import PluginSource
from ..io import IO
from ..utils.manager import ObjectManager

# Third party imports


class PluginLoader:
    """
    Responsible for loading plugins using
    """

    def __init__(self) -> None:
        # Objects
        self.manager = ObjectManager()
        self.io = IO()

    ################################# MODIFIERS #############################

    def load_plugin_using_config(self, plugin_config: PluginConfig) -> bool:
        """
        Load a plugin using information provided in the Config.

        Args:
            plugin_config (Config)

        Returns:
            (bool): True if successful. False otherwise.
        """
        try:
            # Verify that the plugin file exists
            if not self.io.is_file(plugin_config.plugin_file_path):
                return False
            # Read the file in this case
            plugin = self._load_class_from_file(
                plugin_config.plugin_file_path, plugin_config.plugin_source_name,
                plugin_config.plugin_class_name)
            if plugin == None:
                return False
            # save the plugin source.
            plugin_source = PluginSource(
                plugin_config.plugin_name, plugin, plugin_config.plugin_dependencies,
                len(plugin_config.plugin_dependencies),
                plugin_config.plugin_file_path)
            return self._add_plugin(plugin_config.plugin_name, plugin_source)
        except Exception as e:
            print(e)
            pass

    ################################# GETTERS ###############################

    def is_plugin_loaded(self, plugin_name: str) -> bool:
        """
        Determine if the plugin is loaded.

        Args:
            plugin_name (str): Name of the plugin.

        Returns:
            (bool): True if successful. False otherwise.
        """
        return self.manager.is_object(plugin_name)

    def get_loaded_plugin_names(self) -> List[str]:
        """
        Obtain the names of all loaded plugins.

        Returns:
            (List[str]): Names of all plugins.
        """
        return self.manager.get_object_names()

    def get_plugin(self, plugin_name: str) -> Any:
        """
        Obtain the specified plugin.

        Args:
            plugin_name (str)

        Returns:
            (Any)
        """
        if not self.is_plugin_loaded(plugin_name):
            return
        return self.manager.get_object(plugin_name)

    def get_all_plugins(self) -> Dict[str, Any]:
        """
        Obtain all plugins.

        Returns:
            (Dict[str,Any]): Mapping from plugin name to object.
        """
        return self.manager.get_all_objects()

    ######################### PRIVATE METHODS ###############################

    def _add_plugin(self, plugin_name: str, plugin: Any) -> bool:
        """
        Add a plugin with the specified name to the manager.
        """
        return self.manager.add_object(plugin_name, plugin, True)

    def _load_class_from_file(self, file_path: str, module_name: str,
                              class_name: str, *args, **kwargs) -> object:
        """
        Given a file path, load the specified class in the specified module
        from the path. The class is initialized with *args, **kwargs.
        """

        try:
            module_type = imp.load_source(module_name, file_path)
            clazz = getattr(module_type, class_name)
            instance = clazz(*args, **kwargs)
            return instance
        except Exception as e:
            print(e)
