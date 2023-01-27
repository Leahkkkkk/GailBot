from dataclasses import dataclass 
from dict_to_dataclass import field_from_dict, DataclassFromDict
import toml 
import os
@dataclass
class EnginePath(DataclassFromDict):
    watson: str = field_from_dict()
    whisper: str = field_from_dict()

@dataclass 
class SettingsPath(DataclassFromDict):
    default_conf_path: str = field_from_dict()

@dataclass 
class WorkSpace(DataclassFromDict):
    sources_ws: str = field_from_dict()
    settings_ws: str = field_from_dict()
    plugins_ws: str = field_from_dict()
    engines_ws: str = field_from_dict()

config = toml.load(os.path.join(os.getcwd(), "configs/conf.toml"))
ENGINE_PATH = EnginePath.from_dict(config["paths"]["engines"])
SETTING_PATH = SettingsPath.from_dict(config["paths"]["settings"])
WORKSPACE = WorkSpace.from_dict(config["paths"]["workspace"])
