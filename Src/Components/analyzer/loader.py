# Standard library imports
from typing import Dict, Any
# Local imports
from ...utils.loader import Loader
from .plugin_source import PluginSource
from .plugin_config import PluginConfig
from ..io import IO
# Third party imports

class PluginLoader(Loader):

    def __init__(self) -> None:
        super().__init__()
        ## Vars
        self.plugin_class_name = "Plugin"
        self.plugin_source_name = "plugin"
        ## Objects
        self.io = IO()
    ################################# MODIFIERS #############################

    def load_plugin_using_config(self, plugin_config : PluginConfig) -> bool:
        """
        Load a plugin using the specified PluginConfig.

        Args:
            plugin_config (PluginConfig)

        Returns:
            (bool): True if successfully loaded. False otherwise.
        """
        # Verify that the plugin file exists
        if not self.io.is_file(plugin_config.plugin_file_path):
            return False
        # Read the file in this case
        plugin = self._load_class_from_file(
            plugin_config.plugin_file_path,self.plugin_source_name,
            self.plugin_class_name)
        if plugin == None:
            return False
        # save the plugin source.
        plugin_source = PluginSource(
            plugin_config.plugin_name,plugin, plugin_config.plugin_dependencies,
            len(plugin_config.plugin_dependencies),
            plugin_config.plugin_file_path, plugin_config.plugin_author)
        return self._add_plugin(plugin_config.plugin_name,plugin_source)

    ################################# GETTERS ###############################

    def get_plugin(self, plugin_name : str) -> PluginSource:
        """
        Obtain the PluginSource associated with the plugin name.

        Args:
            plugin_name (str)

        Returns:
            (PluginSource)
        """
        return super().get_plugin(plugin_name)

    def get_all_plugins(self) -> Dict[str,PluginSource]:
        """
        Obtain a mapping from plugin name to plugin source for all plugins.

        Returns:
            (Dict[str,PluginSource])
        """
        return super().get_all_plugins()

