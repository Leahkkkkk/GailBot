# Standard library imports
from typing import Callable, Dict, Any
# Local imports
from ....organizer import Settings
from ....io import IO

class GailBotSettings(Settings):

    def __init__(self, data : Dict[str,Any]) -> None:
        self.attrs= [
            "test"]
        super().__init__(attrs=self.attrs)
        self._parse_data(data)

    def save_to_file(self, save_method : Callable[[Dict],bool]) -> bool:
        data = dict()
        for attr in self.attrs:
            data[attr] = self.get(attr)[1]
        return save_method(data)

    def _parse_data(self, data : Dict[str,Any]) -> None:
        for attr, value in data.items():
            self._set_value(attr,value)

