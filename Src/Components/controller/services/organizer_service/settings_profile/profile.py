# Standard imports
# Local imports
from .....organizer import Settings
from ...fs_service import SettingsHook


class SettingProfile:
    """
    SettingProfile object used by OrganizerService.
    """

    def __init__(self, profile_name : str, settings : Settings,
            hook : SettingsHook) -> None:
        """
        Args:
            profile_name (str): Name of the profile.
            settings (Settings)
            hook (SettingsHook)
        """
        self.profile_name : str = profile_name
        self.settings : Settings = settings
        self.hook : SettingsHook = hook

    ############################# MODIFIERS ##################################

    def save(self) -> bool:
        """
        Save the source profile to disk.

        Returns:
            (bool): True if saved successfully, False otherwise.
        """
        return self.hook.save(self.settings)

     ############################# GETTERS ####################################

    def get_profile_name(self) -> str:
        """
        Obtain the name of the profile.
        """
        return self.profile_name

    def get_settings(self) -> Settings:
        """
        Obtain the Settings object associated with the profile.
        """
        return self.settings

    def get_hook(self) -> SettingsHook:
        """
        Obtain the hook associated with the profile.
        """
        return self.hook
