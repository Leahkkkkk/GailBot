# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-06 11:10:05
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-02-17 09:47:50

from typing import List, Dict, Any
from dataclasses import asdict, dataclass, asdict
from .settings import Settings


@dataclass
class GailBotSettings(Settings):

    @dataclass
    class Engines:
        @dataclass
        class WatsonEngine:
            watson_api_key: str = None
            watson_language_customization_id: str = None
            watson_base_language_model: str = None
            watson_region: str = None
        engine_type: str = None
        watson_engine: WatsonEngine = None

    @dataclass
    class Plugins:
        plugins_to_apply: List[str] = None

    @dataclass
    class Core:
        pass

    core: Core = None
    plugins: Plugins = None
    engines: Engines = None

    def to_dict(self) -> Dict:
        return {
            "core": {},
            "plugins": {
                "plugins_to_apply": self.plugins.plugins_to_apply
            },
            "engines": {
                "engine_type": self.engines.engine_type,
                "watson_engine": {
                    "watson_api_key": self.engines.watson_engine.watson_api_key,
                    "watson_language_customization_id": self.engines.watson_engine.watson_language_customization_id,
                    "watson_base_language_model": self.engines.watson_engine.watson_base_language_model,
                    "watson_region": self.engines.watson_engine.watson_region,

                }
            }
        }

    def load_from_dict(self, data: Dict) -> bool:
        try:
            self.core = self.Core()
            self.plugins = self.Plugins(
                data["plugins"]["plugins_to_apply"])
            self.engines = self.Engines(
                data["engines"]["engine_type"],
                self.Engines.WatsonEngine(
                    data["engines"]["watson_engine"]["watson_api_key"],
                    data["engines"]["watson_engine"]["watson_language_customization_id"],
                    data["engines"]["watson_engine"]["watson_base_language_model"],
                    data["engines"]["watson_engine"]["watson_region"]
                )
            )
            return True
        except Exception as e:
            print(e)
            return False
