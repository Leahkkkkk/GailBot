from typing import Any, List, Dict
from gailbot.core.pipeline import Component, ComponentState, ComponentResult
from gailbot.core.utils.general import get_name
from gailbot.plugins import PluginManager, PluginSuite
from gailbot.core.utils.logger import makelogger
import time
from ...converter.result import  ProcessingStats
from ...converter.payload import PayLoadObject
from gailbot.core.pipeline.component import Component
from ...converter.plugin.pluginMethod import GBPluginMethods
logger = makelogger("transcribeComponent")

""" TODO: 
1. connect with a dummy plugin suite and test 

"""
class AnalysisComponent(Component):
    def __init__(self, plugin_manager: PluginManager):
        self.plugin_manager = plugin_manager
        
    def __repr__(self):
        return "Analysis Component"
        
    def __call__(
        self,
        dependency_outputs : Dict[str, Any]
    ) :
        process_start_time = time.time()
        payloads: List[PayLoadObject] = dependency_outputs["transcription"]
        try: 
            for payload in payloads:
                start_time = time.time()
                plugins = payload.setting.get_plugin_setting()
                for plugin in plugins:
                    plugin_suite: PluginSuite = self.plugin_manager.get_suite(plugin)
                    if plugin_suite:
                        method = GBPluginMethods(payload)
                        res = plugin_suite(base_input = None, methods = method)
                end_time = time.time()
                stats = ProcessingStats(
                    start_time=start_time,
                    end_time=end_time,
                    elapsed_time_sec=end_time - start_time
                ) 
                payload.set_analysis_process_stats(stats)    
            
            return ComponentResult(
                state=ComponentState.SUCCESS,
                result=None,
                runtime=0
            )
            
        except Exception as e:
            logger.error(e)
            return ComponentResult(
                state=ComponentState.FAILED,
                result=None,
                runtime=time.time() - process_start_time
            )

                        





