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

    def __init__(self) -> None:
        self.format_manager = ObjectManager()

    ############################### MODIFIERS ################################

    def register_format(self, format_name : str,
            configs : List[Dict[str,Any]]) -> List[str]:
        plugin_manager = PluginManager()
        for config in configs:
            # All the plugins must be registered.
            if not all([plugin_manager.register_plugin_using_config_data(config)]):
                return []
        self.format_manager.add_object(format_name,plugin_manager)
        return plugin_manager.get_plugin_names()

    def apply_format(self, payload : SourcePayload) -> None:
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
            plugin_input = FormatPluginInput(
                payload.get_conversation().get_conversation_name(),
                payload.get_conversation().get_utterances(),
                # TODO: Check the analysis outputs.
                #self._get_analysis_plugin_outputs(payload),
                None,
                payload.get_conversation().get_temp_directory_path(),
                payload.get_conversation().get_result_directory_path())
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
        return self.format_manager.is_object(format_name)

    def get_formats(self) -> List[str]:
        return self.format_manager.get_object_names()

    def is_format_plugin(self, format_name : str, plugin_name : str) -> bool:
        if not self.is_format(format_name):
            return False
        plugin_manager : PluginManager = \
            self.format_manager.get_object(format_name)
        return plugin_manager.is_plugin(plugin_name)

    def get_format_plugins(self, format_name : str) -> List[str]:
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


