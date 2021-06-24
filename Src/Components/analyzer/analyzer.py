# Standard library imports
from typing import Dict, Any, List, Tuple
# Local imports
from .plugin import Plugin
from .loader import PluginLoader
from .logic import PluginPipelineLogic
from .models.config import PluginConfig
from .models.plugin_details import PluginDetails
from .models.plugin_data import PluginData
from .models.apply_config import ApplyConfig
from ..pipeline import Pipeline
# Third party imports

class Analyzer:

    def __init__(self) -> None:
        ## Objects
        self.loader = PluginLoader()

    ############################ MODIFIERS ##################################

    def register_plugin_from_directory(self, plugin_dir_path : str) -> bool:
        return self.loader.load_plugin_from_directory(plugin_dir_path)

    def register_plugin_from_file(self, plugin_config : PluginConfig,
            plugin_file_path : str) -> bool:
        return self.loader.load_plugin_from_file(
            plugin_config, plugin_file_path)

    def register_plugins_in_subdirectories(self, parent_dir_path : str) -> bool:
        return self.loader.load_plugin_subdirectories(parent_dir_path)

    # TODO: Determine args for this.
    def apply_plugins(self, apply_configs : Dict[str, ApplyConfig]) -> Any:
        """
        apply_config structure: plugin_name -> source, workspace.
        """
        # Names of all plugins to apply
        plugin_names = list(apply_configs.keys())
        # All plugins must exist in the loader.
        if not all([self.loader.is_plugin_loaded(name) for name in plugin_names]):
            return
        # Generate the plugin pipeline if all are loaded
        pipeline = self._generate_execution_pipeline(plugin_names)
        pipeline.set_base_input(apply_configs)
        pipeline.execute()

    ############################# GETTERS ###################################

    def is_plugin_loaded(self, plugin_name : str) -> bool:
        return self.loader.is_plugin_loaded(plugin_name)

    def get_loaded_plugin_names(self) -> List[str]:
        return self.loader.get_loaded_plugin_names()

    def get_plugin_details(self, plugin_name : str) -> PluginDetails:
        return self.loader.get_plugin_details(plugin_name)

    def get_all_plugin_details(self) -> Dict[str,PluginDetails]:
        return self.loader.get_all_plugin_details()

    ############################# SETTERS ###################################

    ########################### PRIVATE METHODS #############################

    def _generate_execution_pipeline(self, plugin_names : List[str]) \
            -> Tuple[bool, Pipeline]:
        # TODO: Make sure none of this is hard-coded.
        pipeline = Pipeline("analyzer_pipeline",4)
        pipeline.set_logic(PluginPipelineLogic())
        # Add all components as plugins to the pipeline.
        # TODO: How to deal with plugins with dependencies that have not yet
        # been loaded.
        plugins_data = self.loader.get_all_plugins()
        for plugin_name in plugin_names:
            plugin_data : PluginData = plugins_data[plugin_name]
            if not pipeline.add_component(
                    plugin_name, plugin_data.plugin_object,
                    plugin_data.plugin_dependencies):
                return (False, None)
        return (True, pipeline)

