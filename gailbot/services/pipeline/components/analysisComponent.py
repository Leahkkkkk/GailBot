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
    """ responsible for running plugin after the gailbot obtained the
        transcription result 
    """
    def __init__(self, plugin_manager: PluginManager):
        
        self.plugin_manager = plugin_manager
        
    def __repr__(self):
        return "Analysis Component"
        
    def __call__(
        self,
        dependency_outputs : Dict[str, Any]
    ) :
        """ extract the payloads from the dependency_output and run the 
        
        Args:
            dependency_outputs (Dict[str, Any]): dependency outputs that store 
            the result from the transcription process, which include the 
            payloads data and result state 

        Returns:
            ComponentResult: the result of the analysis process
        """
        process_start_time = time.time()
        logger.info(dependency_outputs)
            
        try: 
            dependency_res: ComponentResult = dependency_outputs["transcription"]
            assert dependency_res.state == ComponentState.SUCCESS
            payloads: List [PayLoadObject] = dependency_res.result
            for payload in payloads:
                logger.info(payload)
                start_time = time.time()
                plugins = payload.setting.get_plugin_setting()
                logger.info(plugins)
                for plugin in plugins:
                    plugin_suite: PluginSuite = self.plugin_manager.get_suite(plugin)
                    if plugin_suite:
                        # create a method that get passed to plugin suite
                        method = GBPluginMethods(payload)
                        res : ComponentResult = plugin_suite(base_input = None, methods = method)
                        assert res.state == ComponentState.SUCCESS
                        
                end_time = time.time()
                stats = ProcessingStats(
                    start_time=start_time,
                    end_time=end_time,
                    elapsed_time_sec=end_time - start_time
                ) 
                payload.set_analysis_process_stats(stats)    
            
            return ComponentResult(
                state  = ComponentState.SUCCESS,
                result = payloads,
                runtime = time.time() - process_start_time
            )
            
        except Exception as e:
            logger.error(e)
            return ComponentResult(
                state=ComponentState.FAILED,
                result=None,
                runtime=time.time() - process_start_time
            )

                        





