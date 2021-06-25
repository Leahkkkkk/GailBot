# Standard library imports
from os import pipe
from typing import Dict, Any, List, Tuple
# Local imports
from .plugin import Plugin
from .loader import PluginLoader
from .logic import PluginPipelineLogic
from .models.config import PluginConfig
from .models.plugin_details import PluginDetails
from .models.plugin_data import PluginData
from .models.apply_config import ApplyConfig
from .models.analyzer_summary import AnalyzerSummary
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
    def apply_plugins(self, apply_configs : Dict[str, ApplyConfig]) \
            -> AnalyzerSummary:
        """
        apply_config structure: plugin_name -> source, workspace.
        """
        # Names of all plugins to apply
        plugin_names = list(apply_configs.keys())
        # All plugins must exist in the loader.
        if not all([self.loader.is_plugin_loaded(name) for name in plugin_names]):
            return
        # Generate the plugin pipeline if all are loaded
        did_generate, pipeline = \
            self._generate_execution_pipeline(apply_configs)
        pipeline.print_dependency_graph()
        pipeline.set_base_input(apply_configs)
        pipeline.execute()
        print(pipeline.get_execution_summary())

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

    def _generate_execution_pipeline(self,
            apply_configs : Dict[str,ApplyConfig]) -> Tuple[bool, Pipeline]:
        # TODO: Make sure none of this is hard-coded.
        pipeline = Pipeline("analyzer_pipeline",4)
        pipeline.set_logic(PluginPipelineLogic())
        print(apply_configs)
        # Add all components as plugins to the pipeline.
        for plugin_name, apply_config in apply_configs.items():
            # Get the current plugin and load all its dependencies.
            if not self._add_plugin_and_dependencies(
                    pipeline,plugin_name,apply_configs):
                return (False,None)
        return (True, pipeline)

    def _add_plugin_and_dependencies(self, pipeline : Pipeline,
            plugin_name : str, apply_configs : Dict[str,ApplyConfig]) -> bool:
        # Plugin must be loaded.
        if not self.loader.is_plugin_loaded(plugin_name) or \
                not plugin_name in apply_configs:
            return False
        # Do not re-load component
        if plugin_name in pipeline.get_component_names():
            return True
        # Load the dependencies
        plugin_data = self.loader.get_plugin(plugin_name)
        dependencies = plugin_data.plugin_dependencies
        for dependency in dependencies:
            if not self._add_plugin_and_dependencies(
                    pipeline,dependency,apply_configs):
                return False
        # Add the actual plugin with all dependencies
        apply_config = apply_configs[plugin_name]
        return pipeline.add_component(
            plugin_name, {
                "plugin_object" : plugin_data.plugin_object,
                "apply_config" : apply_config},
            dependencies)
