# Standard library imports
from enum import Enum
from typing import Callable, Dict, Any, List
from copy import deepcopy
# Local imports
from ...organizer import Settings
from ...io import IO


class GBSettingAttrs(Enum):
    engine_type = "engine_type"
    watson_api_key = "watson_api_key"
    watson_language_customization_id = "watson_language_customization_id"
    watson_base_language_model = "watson_base_language_model"
    watson_region = "watson_region"
    plugins_to_apply = "plugins_to_apply"


class GailBotSettings(Settings):

    def __init__(self, data: Dict[GBSettingAttrs, Any]) -> None:
        self.io = IO()
        self.save_extension = "json"
        self.attrs = list([x for x in GBSettingAttrs])
        self.data = dict()
        self.configured = False
        if not all([attr in data for attr in self.attrs]):
            return
        for attr in self.attrs:
            self.data[attr] = None
        self.configured = True
        for attr, value in data.items():
            self.set_value(attr, value)
    ############################ MODIFIERS ####################################

    def save_to_file(self, save_path: str) -> bool:
        try:
            path_with_extension = "{}.{}".format(
                save_path, self.save_extension)
            data = dict()
            for k, v in self.data.items():
                data[k.value] = v
            return self.io.write(path_with_extension, data, True)
        except:
            return False

    ############################ SETTERS ####################################

    def set_value(self, attr: GBSettingAttrs, value: Any) -> bool:
        if self.has_attribute(attr) and \
                self.is_configured():
            self.data[attr] = value
            return True
        return False

    ############################ GETTERS ####################################

    def is_configured(self) -> bool:
        return self.configured

    def has_attribute(self, attr: GBSettingAttrs) -> bool:
        return attr in self.attrs

    def get_value(self, attr: GBSettingAttrs) -> Any:
        if self.has_attribute(attr) and \
                self.is_configured():
            return self.data[attr]

    def get_all_values(self) -> Dict:
        return deepcopy(self.data)

    ############################ PRIVATE METHODS ##############################
