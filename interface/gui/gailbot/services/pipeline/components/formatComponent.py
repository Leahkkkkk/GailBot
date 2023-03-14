from typing import Any, List, Dict
from gailbot.core.pipeline import Component, ComponentState, ComponentResult
from gailbot.core.utils.logger import makelogger
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
            logger.info(f"format component is run, {len(payloads)} result will be formatted")
            payloads: List [PayLoadObject] = dependency_res.result
            logger.info(payloads)
            for payload in payloads:
                logger.info(f"saving {payload.name} result to {payload.out_dir}")
                payload.save()
            
            assert dependency_res.state == ComponentState.SUCCESS    
            return ComponentResult(
                state = ComponentState.SUCCESS,
                result = payloads,
                runtime = 0
            )
         
        except Exception as e:
            logger.error(f"error in formatting payload result {e}")
            return ComponentResult(
                state=ComponentState.FAILED,
                result=None,
                runtime=0
            )

    def __repr__(self):
        return "Format component"