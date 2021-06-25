# Standard library imports
from typing import Dict, Any, List, Tuple
# Local imports
from .loader import PluginLoader
from .logic import PluginPipelineLogic
from .plugin_config import PluginConfig
from .plugin_source import PluginSource
from .apply_config import ApplyConfig
from .analysis_summary import AnalysisSummary
from .plugin_execution_summary import PluginExecutionSummary
from ..io import IO
from ..pipeline import Pipeline, Stream
# Third party imports

class Analyzer:

    def __init__(self) -> None:
        ## Objects
        self.loader = PluginLoader()
        self.io = IO()
        ## Vars
        self.config_file_extension = "json"
        self.pipeline_name = "analyzer_pipeline"
        self.pipeline_num_threads = 3

    ############################ MODIFIERS ##################################

    def register_plugins_from_directory(self, dir_path : str,
            check_subdirectories : bool = True) -> int:
        if not self.io.is_directory(dir_path):
            return 0
        # Load all possible config files
        _, paths = self.io.path_of_files_in_directory(
            dir_path,[self.config_file_extension],check_subdirectories)
        return len([self.register_plugin_using_config_file(path) for path in paths])

    def register_plugin_using_config_file(self, config_file_path : str) -> bool:
        # Generate config object and load
        try:
            _ , data = self.io.read(config_file_path)
            config = PluginConfig(
                data["plugin_name"], data["plugin_dependencies"],
                data["plugin_file_path"], data["plugin_author"])
            return self.loader.load_plugin_using_config(config)
        except:
            return False

    def apply_plugins(self, apply_configs : Dict[str, ApplyConfig]) \
            -> AnalysisSummary:
        did_generate, pipeline = self._generate_execution_pipeline(
            apply_configs)
        if not did_generate:
            return False
        pipeline.set_base_input(apply_configs)
        pipeline.execute()
        return self._generate_analysis_summary(pipeline.get_execution_summary())

    ############################# GETTERS ###################################

    def is_plugin(self, plugin_name : str) -> bool:
        return self.loader.is_plugin_loaded(plugin_name)

    def get_plugin_names(self) -> List[str]:
        return self.loader.get_loaded_plugin_names()

    ########################### PRIVATE METHODS #############################

    def _generate_execution_pipeline(self,
            apply_configs : Dict[str,ApplyConfig]) -> Tuple[bool, Pipeline]:
        pipeline = Pipeline(self.pipeline_name,self.pipeline_num_threads)
        pipeline.set_logic(PluginPipelineLogic())
        for plugin_name in apply_configs.keys():
            if not self._add_plugin_with_dependencies(
                    pipeline,plugin_name,apply_configs):
                return (False,None)
        return (True, pipeline)

    def _add_plugin_with_dependencies(self, pipeline : Pipeline,
            plugin_name : str, apply_configs : Dict[str,ApplyConfig]) -> bool:
        # Plugin must be loaded.
        if not self.loader.is_plugin_loaded(plugin_name) or \
                not plugin_name in apply_configs:
            return False
        # Do not re-load component
        if plugin_name in pipeline.get_component_names():
            return True
        # Load the dependencies
        plugin_source : PluginSource = self.loader.get_plugin(plugin_name)
        for dependency in plugin_source.plugin_dependencies:
            if not self._add_plugin_and_dependencies(
                    pipeline,dependency,apply_configs):
                return False
        # Add actual plugin
        return pipeline.add_component(
            plugin_name, plugin_source,plugin_source.plugin_dependencies)

    def _generate_analysis_summary(self, execution_summary : Dict[str,Any]) \
            -> AnalysisSummary:
        # Generating the plugin summaries.
        plugin_summaries = dict()
        for component_name, summary in execution_summary.items():
            stream : Stream = summary["result"]
            plugin_summaries[component_name] = stream.get_stream_data()
        # Geerating the analysis summary
        total_time_seconds = 0
        successful_plugins = list()
        failed_plugins = list()
        for plugin_summary in plugin_summaries.values():
            plugin_summary : PluginExecutionSummary
            total_time_seconds += plugin_summary.runtime_seconds
            if plugin_summary.was_successful:
                successful_plugins.append(plugin_summary.plugin_name)
            else:
                failed_plugins.append(plugin_summary.plugin_name)
        return AnalysisSummary(
            total_time_seconds,successful_plugins,failed_plugins,
            plugin_summaries)


