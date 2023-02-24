from typing import Any, List, Dict
from gailbot.core.pipeline import Component, ComponentState, ComponentResult
from gailbot.core.utils.general import (
    get_name
)
from gailbot.plugins import PluginManager
from gailbot.core.utils.logger import makelogger
import time
from ...converter.result import  ProcessingStats
from ...converter.payload import PayLoadObject
logger = makelogger("transcribeComponent")
from gailbot.core.pipeline.component import Component

""" TODO: 
1. connect with a dummy plugin suite and test 
"""
class AnalysisComponent(Component):
    def __init__(self, plugin_manager: PluginManager):
        self.plugin_manager = plugin_manager
        
    def __repr__(self):
        raise NotImplementedError()

    def __call__(
        self,
        dependency_outputs : Dict[str, Any]
    ) :
       raise NotImplementedError()





