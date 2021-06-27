# Standard library imports
from typing import List, Dict
# Local imports
from ....analyzer import Analyzer,AnalysisSummary,ApplyConfig,PluginConfig
from ....organizer import Conversation
from .....utils.manager import ObjectManager
from .....utils.threads import ThreadPool
from .transcribable import Transcribable
# Third party imports


class AnalysisStage:

    def __init__(self) -> None:
        ## Vars.
        ## Objects
        self.analyzer = Analyzer()
        self.transcribables = ObjectManager()
        self.thread_pool = ThreadPool(4)
        self.thread_pool.spawn_threads()

    ########################### MODIFIERS ###################################

    def register_plugins_from_directory(self, dir_path : str) -> int:
        return self.analyzer.register_plugins_from_directory(dir_path,True)

    def add_transcribable(self, transcribable : Transcribable) -> bool:
        return self.transcribables.add_object(
            transcribable.identifier,transcribable)

    def add_transcribables(self, transcribables : List[Transcribable]) -> bool:
        return all([self.add_transcribable(transcribable) \
            for transcribable in transcribables])

    def analyze(self) -> None:
        plugin_names = self.analyzer.get_plugin_names()
        transcribables = self.transcribables.get_all_objects()
        for _, transcribable in transcribables.items():
            apply_configs = dict()
            for plugin_name in plugin_names:
                apply_configs[plugin_name] = self._generate_apply_config(
                    plugin_name, transcribable)
            self.thread_pool.add_task(
                self._analyze_thread,[apply_configs],{})
        self.thread_pool.wait_completion()

    ############################# GETTERS ###################################


    ############################# SETTERS ###################################


    ######################## PRIVATE METHODS ################################

    def _generate_apply_config( plugin_name : str,
            transcribable : Transcribable) -> ApplyConfig:
        return ApplyConfig(
            plugin_name,
            transcribable.source_to_transcribable_map.values(),
            transcribable.conversation.get_temp_directory_path(),
            transcribable.conversation.get_result_directory_path())

    def _analyze_thread(self, apply_configs : Dict[str,ApplyConfig]) -> None:
        summary = self.analyzer.apply_plugins(apply_configs)


