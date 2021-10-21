from abc import ABC, abstractmethod
from typing import Any, Dict


class Settings(ABC):

    def __init__(self, data: Dict) -> None:
        pass

    def is_configured(self) -> bool:
        pass

    def has_attribute(self, attr: str) -> bool:
        pass

    def set_value(self, attr: str, value: Any) -> bool:
        pass

    def get_value(self, attr: str) -> Any:
        pass

    def get_all_values(self) -> Dict:
        pass

    def save_to_file(self, save_path: str) -> None:
        pass
