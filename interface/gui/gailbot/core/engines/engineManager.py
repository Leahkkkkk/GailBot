# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-10 13:29:08
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-16 15:02:59
from typing import Dict, List, Any
from gailbot.core.engines import (
    Engine,
    Watson,
    Google,
    WhisperEngine
)

_ENGINES = {
    "watson" : Watson,
    "google" : Google,
    "whisper" : WhisperEngine
}

class EngineManager:
    """ 
    provides wrapper function to run available speech detect engines
    """
    def available_engines(self) -> List[str]:
        """
        Returns:
            List[str]: return a list of available engine
        """
        return list(_ENGINES.keys())

    def is_engine(self, name : str) -> bool:
        return name in self.available_engines()

    def init_engine(self, name : str, **kwargs) -> Engine:
        if not self.is_engine(name):
            raise Exception(
                f"Engine not supported: {name}"
            )
        engine = _ENGINES[name](**kwargs)
        return engine