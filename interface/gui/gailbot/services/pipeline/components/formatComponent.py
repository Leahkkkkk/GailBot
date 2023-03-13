from typing import Any, List, Dict
from gailbot.core.pipeline import Component, ComponentState, ComponentResult
from gailbot.core.utils.logger import makelogger
import time
from ...converter.result import  ProcessingStats
from ...converter.payload import PayLoadObject
logger = makelogger("transcribeComponent")

class FormatComponent(Component):
    def __call__(
        self,
        dependency_outputs : Dict[str, Any]
    ) -> ComponentState:

        """
        Gets a source and the associated settings objects and transcribes it
        
        Args:
            dependency_outputs : Dict[str, Any]: output of the dependency map to search through

        Returns: 
            ComponentResult: the result of the formatting process
        """
        try:
            dependency_res: ComponentResult = dependency_outputs["analysis"]
            assert dependency_res.state == ComponentState.SUCCESS
            payloads: List [PayLoadObject] = dependency_res.result
            logger.info(payloads)
            for payload in payloads:
                payload.save()
                
            return ComponentResult(
                state = ComponentState.SUCCESS,
                result = payloads,
                runtime = 0
            )
         
        except Exception as e:
            logger.error(e)
            return ComponentResult(
                state=ComponentState.FAILED,
                result=None,
                runtime=0
            )

    def __repr__(self):
        return "Format component"