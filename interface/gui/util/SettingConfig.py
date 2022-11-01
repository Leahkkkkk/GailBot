from dataclasses import dataclass 
from os.path import exists
import toml 

from dict_to_dataclass import DataclassFromDict, field_from_dict

# config = toml.load("../controller/interface.toml")
config = toml.load("controller/interface.toml")


@dataclass 
class ProfileSetting(DataclassFromDict):
    RequiredSetting: dict = field_from_dict()
    PostTranscribe: dict = field_from_dict()
    Plugins: dict = field_from_dict()
    

ProfileSettingForm = ProfileSetting.from_dict(config["profile form"])

print(ProfileSettingForm)