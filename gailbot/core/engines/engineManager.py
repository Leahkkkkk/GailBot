# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-10 13:29:08
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-16 15:02:59

# NOTE: why would engine manger be under here instead of under engine folder, 
# mirroring the structure for plugin? 
import sys
import os
from typing import Dict, List, Any
from gailbot.core.engines import (
    Engine,
    Watson,
    Google,
    WhisperEngine
    
)
from gailbot.core.utils.general import (
    make_dir
)

_ENGINES = {
    "watson" : Watson,
    "google" : Google,
    "whisper" : WhisperEngine
}

class EngineManager:
    def available_engines(self) -> List[str]:
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