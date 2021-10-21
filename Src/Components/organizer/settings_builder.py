# Standard library imports
from typing import Any, Dict, List, Tuple, Callable
from copy import deepcopy
# Local imports
from .settings import Settings
# Third party imports


class SettingsBuilder:
    """
    Responsible for constructing and performing different operations on
    Settings objects.
    """

    def __init__(self) -> None:
        self.setting_creators = dict()

    def register_setting_type(self, settings_type: str,
                              setting_creator: Callable[[Any], Settings]) \
            -> bool:
        """
        Register a new type of settings if it is not already registered.

        Args:
            settings_type (str): Type of the new settings.
            settings_creator (Callable[[Any],Settings])

        Returns:
            (bool):
                True if successful. False otherwise or if settings_type
                was previously registered.
        """
        if settings_type in self.setting_creators:
            return False
        self.setting_creators[settings_type] = setting_creator
        return True

    def remove_registered_settings_type(self, settings_type: str) -> None:
        if self.is_registered_settings_type(settings_type):
            del self.setting_creators[settings_type]

    def is_registered_settings_type(self, settings_type: str) -> bool:
        return settings_type in self.setting_creators

    def get_registered_setting_types(self) -> Dict[str, Settings]:
        """
        Obtain a mapping from a setting type to its creator.

        Returns:
            (Dict[str,Settings]): Mapping from setting type to creator.
        """
        return deepcopy(self.setting_creators)

    def create_settings(self, settings_type: str, data: Dict[str, str]) \
            -> Tuple[bool, Settings]:
        """
        Generate a Settings object from the provided data.
        The data must only contain SettingsAttributes as keys and their
        associated values.

        Args:
            data (Dict[str,str]):
                Mapping from SettingsAttributes string values to their
                actual values

        Returns:
            (Tuple[bool,Settings]):
                True + Settings object if successful.
                False + None if unsuccessful.
        """
        if not settings_type in self.setting_creators:
            return (False, None)
        try:
            settings: Settings = self.setting_creators[settings_type](data)
            if not settings.is_configured():
                return (False, None)
            return (True, settings)
        except Exception as e:

            return (False, None)

    def copy_settings(self, settings: Settings) -> Settings:
        """
        Returns a copy of the given Settings object, with all internal
        attributes copied.

        Args:
            settings (Settings)

        Returns:
            (Settings): Copy of the original Settings object.
        """
        return deepcopy(settings)

    def change_settings(self, settings: Settings, data: Dict[str, str]) \
            -> bool:
        """
        Change the attributes with the provided data of the given settings
        object.
        Settings object attributes CANNOT be changed directly.

        Args:
            settings (Settings): Object whose attributes to change.
            data (Dict[str,str]):
                Mapping from SettingsAttributes string values to their
                actual values

        Returns:
            (bool): True if successful. False otherwise.
        """
        # The settings item must have a items dictionary
        for k, v in data.items():
            if not settings.has_attribute(k):
                return False
        for k, v in data.items():
            if not settings.set_value(k, v):
                return False
        return settings.is_configured()

    ################################# PRIVATE METHODS ##########################
