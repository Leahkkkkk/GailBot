# Standard library imports
from typing import Callable, Dict, Any, List
from enum import Enum
# Local imports
from .....organizer import Settings
from .gb_settings_attrs import GBSettingAttrs

class GailBotSettings(Settings):

    def __init__(self, data : Dict[str,Any]) -> None:
        self.attrs = [e.value for e in GBSettingAttrs]
        super().__init__(attrs=self.attrs)
        self._parse_data(data)

    ############################ MODIFIERS ####################################

    def save_to_file(self, save_method : Callable[[Dict],bool]) -> bool:
        data = dict()
        for attr in self.attrs:
            data[attr] = self.get(attr)[1]
        return save_method(data)

    ############################ SETTERS ####################################

    def set_using_attribute(self, attr : GBSettingAttrs, value : Any) -> bool:
        return self.set(attr.value,value)

    def set_engine_type(self, engine_type : str) -> bool:
        return self.set(GBSettingAttrs.engine_type,engine_type)

    def set_watson_api_key(self, key : str) -> bool:
        return self.set("watson_api_key",key)

    def set_watson_language_customization_id(self, id : str) -> bool:
        return self.set("watson_language_customization_id",id)

    def set_watson_base_language_model(self, base_model_name : str) -> bool:
        return self.set("watson_base_language_model",base_model_name)

    def set_watson_region(self, region : str) -> bool:
        return self.set("watson_region",region)

    def set_output_format(self, output_format : str) -> bool:
        return self.set("output_format", output_format)

    def set_analysis_plugins_to_apply(self, analysis_plugins : List[str]) -> bool:
        return self.set("analysis_plugins_to_apply", analysis_plugins)

    ############################ GETTERS ####################################

    def get_all_values(self) -> Dict[str,Any]:
        values = dict()
        for attr in self.attrs:
            values[attr] = self.get(attr)[1]
        return values

    def get_engine_type(self) -> str:
        return self.get("engine_type")[1]

    def get_watson_api_key(self) -> str:
        return self.get("watson_api_key")[1]

    def get_watson_language_customization_id(self) -> str:
        return self.get("watson_language_customization_id")[1]

    def get_watson_base_language_model(self) -> str:
        return self.get("watson_base_language_model")[1]

    def get_watson_region(self) -> bool:
        return self.get("watson_region")[1]

    def get_output_format(self) -> str:
        return self.get("output_format")[1]

    def get_analysis_plugins_to_apply(self) -> List[str]:
        return self.get("analysis_plugins_to_apply")[1]

    ############################ PRIVATE METHODS ##############################

    def _parse_data(self, data : Dict[str,Any]) -> None:
        for attr, value in data.items():
            self._set_value(attr,value)

