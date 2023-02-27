from dataclasses import dataclass
from dict_to_dataclass import field_from_dict, DataclassFromDict
import toml 
from typing import List, Dict

@dataclass
class FileExtensions(DataclassFromDict):
    supported: List = field_from_dict()
    output: str = field_from_dict()
    saveGB: str = field_from_dict()

@dataclass
class ConversationDirText(DataclassFromDict):
    dir: str = field_from_dict()

@dataclass
class TransDirTest(DataclassFromDict):
    transDir: str = field_from_dict()

@dataclass
class ResultText(DataclassFromDict):
    transResult: str = field_from_dict()
    tempResult: str = field_from_dict()

@dataclass 
class InterfaceText(DataclassFromDict):
    engine: str = field_from_dict()
    notFound: str = field_from_dict()
    googleName: str = field_from_dict()
    watsonName: str = field_from_dict()
    whisperName: str = field_from_dict()
    engine_setting: str = field_from_dict()
    plugin_setting: str = field_from_dict()

@dataclass
class DefaultSettings(DataclassFromDict):
    default: Dict = field_from_dict()

def load_file_extensions(path: str):
    d = toml.load(path)
    return FileExtensions.from_dict(d["converter.fileExtensions"])

def load_conversation_payload(path: str):
    d = toml.load(path)
    return ConversationDirText.from_dict(d["dir_payload"])

def load_transdir_payload(path: str):
    d = toml.load(path)
    return TransDirTest.from_dict(d["trans_dir_payload"])

def load_result(path: str):
    d = toml.load(path)
    return ResultText.from_dict(d["result"])

def load_interfaces(path: str):
    d = toml.load(path)
    return InterfaceText.from_dict(d["organizer.interfaces"])

def load_default_settings(path: str):
    d = toml.load(path)
    return DefaultSettings.from_dict(d["settings.default"])