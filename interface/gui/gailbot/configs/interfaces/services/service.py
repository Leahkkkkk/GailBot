from dataclasses import dataclass
from dict_to_dataclass import field_from_dict, DataclassFromDict
import toml 
from typing import List, Dict

@dataclass
class DirectoryName(DataclassFromDict): 
      temp_extension                   : str = field_from_dict()
      output_extension                 : str = field_from_dict()
      hidden_file                      : str = field_from_dict()
      trans_result                     : str = field_from_dict()
      temp_result                      : str = field_from_dict()
      analysis_result                  : str = field_from_dict()
@dataclass
class Engines(DataclassFromDict): 
      engine                     : str = field_from_dict()
      google_name                : str = field_from_dict()
      watson_name                : str = field_from_dict()
      whisper_name               : str = field_from_dict()
      audio_supported_format     : List[str] = field_from_dict()

@dataclass 
class Thread(DataclassFromDict): 
      transcriber_num_threads  : int = field_from_dict()
      payload_num_threads      : int = field_from_dict()
      analysis_num_threads     : int = field_from_dict()
@dataclass
class ServiceConfig(DataclassFromDict):
    engines : Engines = field_from_dict()
    directory_name : DirectoryName = field_from_dict()
    thread : Thread = field_from_dict()

@dataclass 
class ProfileData(DataclassFromDict):
    plugin_setting: List[str] = field_from_dict()
    engine_setting_name: str = field_from_dict()
@dataclass 
class DefaultSetting(DataclassFromDict): 
    profile_name                     : str = field_from_dict()
    profile_data                     : dict = field_from_dict()
    engine_name                      : str = field_from_dict() 
    engine_data                      : dict = field_from_dict()
    profile_data_no_plugin           : dict = field_from_dict()


def load_service_config(path: str) -> ServiceConfig:
    d = toml.load(path)
    return ServiceConfig.from_dict(d)

def load_default_setting(path: str) -> DefaultSetting:
    d = toml.load(path)
    return DefaultSetting.from_dict(d)