# Standard imports
# Local imports
from .....organizer import Settings
from ...fs_service import SettingsHook


class SettingProfile:

    def __init__(self, profile_name : str, settings : Settings,
            hook : SettingsHook) -> None:
        self.profile_name : str = profile_name
        self.settings : Settings = settings
        self.hook : SettingsHook = hook

    ############################# MODIFIERS ##################################

    def save(self) -> bool:
        return self.hook.save(self.settings)


     ############################# GETTERS ####################################

    def get_profile_name(self) -> str:
        return self.profile_name

    def get_settings(self) -> Settings:
        return self.settings

    def get_hook(self) -> SettingsHook:
        return self.hook
