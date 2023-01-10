# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-10 13:29:08
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-10 14:17:44


import sys
import os
from typing import Dict, List, Any
from core.engines import Engine

class EngineManager:

    def __init__(
        self,
        engine_ws_path : str,
        engine_conf_paths : str
    ):
        pass

    def available_engines(self) -> List[str]:
        pass

    def is_engine(self, name : str) -> bool:
        pass

    def init_engine(self, name : str, conf : Dict = None) -> Engine:
        pass