import time
from typing import Any, List, Dict

from gailbot.core.utils.logger import makelogger
from gailbot.core.pipeline import Component, ComponentState, ComponentResult
from gailbot.core.utils.threads import ThreadPool

from gailbot.plugins import PluginManager, PluginSuite
from gailbot.services.converter.result import  ProcessingStats
from gailbot.services.converter.payload import PayLoadObject
from ...converter.plugin.pluginMethod import GBPluginMethods
from ..components.progress import ProgressMessage
from gailbot.configs import service_config_loader


NUM_THREAD = service_config_loader().thread.analysis_num_threads
logger = makelogger("analysisComponent")

class PluginError(Exception):
    def __init__(self, msg) -> None:
        self.msg = msg 
        
    def __repr__(self) -> str:
        return f"Plugin Error: {self.msg}"
    
    def __str__(self) -> str:
        return f"Plugin Error: {self.msg}"
class AnalysisComponent(Component):
    """ Responsible for running plugin after gailbot has obtained the
        transcription result 
    """
    def __init__(self, plugin_manager: PluginManager):
        self.plugin_manager = plugin_manager
        
    def __repr__(self):
        return "Analysis Component"
        
    def __call__(
        self,
        dependency_outputs : Dict[str, Any]
    ) -> ComponentResult:
        """ 
        Extracts the payloads from the dependency_output and runs the analysis
        
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
            logger.info(f"result from transcription {dependency_res}")
            assert dependency_res.state == ComponentState.SUCCESS
            
            payloads: List [PayLoadObject] = dependency_res.result
            logger.info(f"get payloads {payloads}")
            for payload in payloads:
                if not payload.failed:
                    self.analyze_payload(payload)
    
            return ComponentResult(
                state  = ComponentState.SUCCESS,
                result = payloads,
                runtime = time.time() - process_start_time)
            
        except Exception as e:
            logger.error(e, exc_info=e)
            return ComponentResult(
                state = ComponentState.FAILED,
                result = payloads,
                runtime = time.time() - process_start_time
            )

    def analyze_payload(self, payload: PayLoadObject):
        logger.info("start analyzing payload")
        # self.emit_progress(payload, ProgressMessage.Analyzing)
        start_time = time.time()
        plugins = payload.setting.get_plugin_setting()
        logger.info(f"the following plugins are applied: {plugins}")
        if not plugins:
            return True
        # try applying plugin
        try:
            for plugin in plugins:
                plugin_suite: PluginSuite = self.plugin_manager.get_suite(plugin)
                # check plugin suit is valid
                if not plugin_suite:
                    self.emit_progress(payload, f"{plugin} is not a valid plugin")
                    raise PluginError(f"{plugin} is not a valid plugin")
                
                logger.info(f"retrieved plugin suite {plugin_suite}")
                
                # create a method that get passed to plugin suite, and apply plugin suite
                method = GBPluginMethods(payload)
                res : Dict[str, ComponentState] = plugin_suite(base_input = None, methods = method)
                
                logger.info(f"get the plugin result {res}")
                for state in res.values():
                    assert state == ComponentState.SUCCESS
            end_time = time.time()
            stats = ProcessingStats(
                start_time=start_time,
                end_time=end_time,
                elapsed_time_sec=end_time - start_time
            ) 
            payload.set_analysis_process_stats(stats)   
        except Exception as e:
            logger.error(f"fail to apply the plugin suite {plugin}, error {e}", exc_info=e)
            self.emit_progress(payload, ProgressMessage.Error)
            payload.set_failure()
            return False 
        else:
            payload.set_analyzed()
            return True
        
    def emit_progress(self, payload: PayLoadObject, msg: str):
        if payload.progress_display:
            payload.progress_display(msg)

                        





