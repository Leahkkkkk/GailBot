from typing import Any, List, Dict
from gailbot.core.pipeline import Component, ComponentState, ComponentResult
from gailbot.core.utils.general import get_name
from gailbot.plugins import PluginManager, PluginSuite
from gailbot.core.utils.logger import makelogger
import time
from ...converter.result import  ProcessingStats
from ...converter.payload import PayLoadObject
from gailbot.core.pipeline.component import Component
from ...converter.plugin.pluginMethod import GBPluginMethods, get_plugin_methods
from gailbot.core.utils.threads import ThreadPool
from ..components.progress import ProgressMessage
logger = makelogger("transcribeComponent")

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
           
            for payload in payloads:
                # for each payload, check if the last stage is successful
                if not payload.failed: 
                    self.emit_progress(payload, ProgressMessage.Analyzing)
                    
                    # a list of plugin methods
                    methods: List[GBPluginMethods] = get_plugin_methods(payload)
                    
                    start_time = time.time()
                    plugins = payload.setting.get_plugin_setting()
                    
                    num_plugins = len(plugins)
                    num_file = len(methods)
                    logger.info(f"the following plugins are applied: {plugins}")
                
                    # try applying plugin
                    try:
                        for idx, plugin in enumerate (plugins):
                            plugin_res = dict()
                            threadpool = ThreadPool(5)  # TODO: analysis in parallel 
                            plugin_suite: PluginSuite = self.plugin_manager.get_suite(plugin)
                            # check plugin suit is valid
                            if not plugin_suite:
                                raise PluginError(f"{plugin} is not a valid plugin suite")
                         
                            logger.info(f"retrieved plugin suite {plugin_suite}")
                            self.emit_progress(payload, f"Applying plugin suite {plugin}")
                            
                            # create a method that get passed to plugin suite, and apply plugin suite
                            for idx, method in enumerate(methods):
                                res : Dict[str, ComponentState] = plugin_suite(base_input = None, methods = method)
                                plugin_res[method.filename] = res 
                                logger.info(f"get the plugin result {res}")
                                for state in res.values():
                                    if not state == ComponentState.SUCCESS: 
                                        raise PluginError(f"{plugin} is not applied successfully")
                                self.emit_progress(payload, f"{idx + 1} / {num_file} files are analyzed by {plugin_suite.name} plugin ")
                            
                            self.emit_progress(payload, f"{idx + 1} / {num_plugins} plugin suites applied")
                            
                        end_time = time.time()
                        stats = ProcessingStats(
                            start_time=start_time,
                            end_time=end_time,
                            elapsed_time_sec=end_time - start_time
                        ) 
                        
                        payload.set_analysis_process_stats(stats)   
                        
                    except Exception as e:
                        logger.error(f"fail to get the plugin suite {plugin}, error {e}", exc_info=e)
                        self.emit_progress(payload, ProgressMessage.Error)
                        payload.set_failure()
                    
                    else:
                        payload.set_analyzed()
                    
            return ComponentResult(
                state  = ComponentState.SUCCESS,
                result = payloads,
                runtime = time.time() - process_start_time)
            
        except Exception as e:
            logger.error(e, exc_info=e)
            return ComponentResult(
                state=ComponentState.FAILED,
                result= payloads,
                runtime=time.time() - process_start_time
            )

    def emit_progress(self, payload: PayLoadObject, msg: str):
        if payload.progress_display:
            payload.progress_display(msg)

                        





