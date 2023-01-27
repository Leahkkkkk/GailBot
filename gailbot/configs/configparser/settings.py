from dataclasses import dataclass 
from dict_to_dataclass import field_from_dict, DataclassFromDict
from typing import List
from configs.conf_path import SETTING_PATH
import toml 

@dataclass 
class Plugin(DataclassFromDict):
    suit: str = field_from_dict()
    apply_plugins: List[str] = field_from_dict()


@dataclass 
class Whisper(DataclassFromDict):
    some_ley: str = field_from_dict()
    


@dataclass 
class WatsonInitialization(DataclassFromDict):
    apikey: int = field_from_dict()
    region: int = field_from_dict()


@dataclass 
class WatsonTranscribe(DataclassFromDict):
    base_model : int = field_from_dict()
    language_customization_id : int = field_from_dict()
    acoustic_customization_id : int = field_from_dict()


setting_data = toml.load(SETTING_PATH.default_conf_path)

@dataclass
class Watson(DataclassFromDict):
    initialize: WatsonInitialization = WatsonInitialization.from_dict(setting_data["engine"]["watson"]["initialization"])
    transcribe: WatsonTranscribe = WatsonTranscribe.from_dict(setting_data["engine"]["watson"]["transcribe"])
    
@dataclass 
class Engine:
    name: setting_data["engine"]["name"]
    whisper: Whisper = Whisper.from_dict(setting_data["engine"]["whisper"])
    watson: Watson = Watson
    
@dataclass 
class Setting:
    plugins: Plugin = Plugin.from_dict(setting_data["plugins"])
    engine:  Engine = Engine