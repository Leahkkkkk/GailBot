from typing import Any
from dataclasses import dataclass
from ...config import Config, ConfigLoader, BlackBoard

# ------------ Blackboards


@dataclass
class PipelineBlackBoard(BlackBoard):
    RAW_EXTENSION: str
    METADATA_NAME: str
    METADATA_EXTENSION: str


class PipelineConfigLoader(ConfigLoader):
    def load_blackboard(self, blackboard_data: Any) -> BlackBoard:
        try:
            return PipelineBlackBoard(
                blackboard_data["raw_extension"],
                blackboard_data["metadata_name"],
                blackboard_data["metadata_extension"]
            )
        except:
            raise Exception()


@dataclass
class ServicesBlackBoard(BlackBoard):
    DEFAULT_SETTINGS_TYPE: str


class ServicesConfigLoader(ConfigLoader):
    def load_blackboard(self, blackboard_data: Any) -> BlackBoard:
        try:
            return ServicesBlackBoard(
                blackboard_data["default_settings_type"]
            )
        except:
            raise Exception()
