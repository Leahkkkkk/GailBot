# Standard imports
from typing import List, Dict, Any
# Local imports
from ......utils.threads import ThreadPool
from ......utils.manager import ObjectManager
from .....plugin_manager import PluginManager, PluginManagerSummary, ApplyConfig
from ...organizer_service import GailBotSettings, RequestType
from ..pipeline_payload import SourcePayload
from .format_plugin_input import FormatPluginInput

class FormatStage:
    """
    Applies different format plugins to the payload.
    """

    def __init__(self) -> None:
        self.format_manager = ObjectManager()

    ############################### MODIFIERS ################################

    def register_format(self, format_name : str,
            configs : List[Dict[str,Any]]) -> List[str]:
        """
        Register a format with the specified name using a list of configuration
        dictionaries.

        Args:
            format_name (str): Name of the format.
            configs (List[Dict[str,Any]]):
                List of config dictionary objects.

        Returns:
            (List[str]): List of plugin names that were registered.
        """
        plugin_manager = PluginManager()
        for config in configs:
            # All the plugins must be registered.
            if not all([plugin_manager.register_plugin_using_config_data(config)]):
                return []
        self.format_manager.add_object(format_name,plugin_manager)
        return plugin_manager.get_plugin_names()

    def apply_format(self, payload : SourcePayload) -> None:
        """
        Apply format plugins, determined using the settings profile, to the
        payload.

        Args:
            payload (SourcePayload)
        """
        if not self._can_format(payload):
            msg = "[{}] [Format stage] Unable to format".format(
                payload.get_source_name())
            payload.log(RequestType.FILE,msg)
            payload.set_format_status(False)
        # Apply the appropriate format
        settings : GailBotSettings = payload.get_conversation().get_settings()
        output_format = settings.get_output_format()
        plugin_manager : PluginManager = self.format_manager.get_object(
            output_format)
        # Generate apply configs for all format plugins.
        apply_configs = dict()
        for plugin_name in plugin_manager.get_plugin_names():
            plugin_input = FormatPluginInput(payload)
            apply_configs[plugin_name] = ApplyConfig(
                plugin_name,[plugin_input],{})
        # Apply all the plugins
        manager_summary : PluginManagerSummary = \
            plugin_manager.apply_plugins(apply_configs)
        payload.set_format_plugin_summaries(manager_summary.plugin_summaries)
        if all([plugin_name in manager_summary.successful_plugins \
                for plugin_name in apply_configs.keys()]):
            msg = "[{}] [Format stage] Successful with plugins: {}".format(
                payload.get_source_name(),list(apply_configs.keys()))
            payload.set_format_status(True)
        else:
            msg = "[{}] [Format stage] Unsuccessful".format(
                payload.get_source_name())
        payload.log(RequestType.FILE,msg)

    ########################## GETTERS #########################################

    def is_format(self, format_name : str) -> bool:
        """
        Determine if the format exists.

        Args:
            format_name (str)

        Returns:
            (bool): True if format exists, False otherwise.
        """
        return self.format_manager.is_object(format_name)

    def get_formats(self) -> List[str]:
        """
        Obtain a list of all registered formats.

        Returns:
            (List[str])
        """
        return self.format_manager.get_object_names()

    def is_format_plugin(self, format_name : str, plugin_name : str) -> bool:
        """
        Determine if the plugin exists for the specified format.

        Args:
            format_name (str): Name of registered format.
            plugin_name (str): Name of the plugin to check for.

        Returns:
            (bool): True if the plugin exists for the format, False otherwise.
        """
        if not self.is_format(format_name):
            return False
        plugin_manager : PluginManager = \
            self.format_manager.get_object(format_name)
        return plugin_manager.is_plugin(plugin_name)

    def get_format_plugins(self, format_name : str) -> List[str]:
        """
        Obtain the names of all plugins associated with the given format.

        Args:
            format_name (str)

        Returns:
            (List[str]): Names of all plugins associated with this format.
        """
        if not self.is_format(format_name):
            return []
        plugin_manager : PluginManager = \
            self.format_manager.get_object(format_name)
        return plugin_manager.get_plugin_names()

    ######################## PRIVATE METHODS ##################################

    def _can_format(self, payload : SourcePayload) -> bool:
        settings : GailBotSettings = payload.get_conversation().get_settings()
        output_format = settings.get_output_format()
        return self.is_format(output_format)



