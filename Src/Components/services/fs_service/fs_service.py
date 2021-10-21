# Standard library imports
from typing import Dict, List, Any
from .hooks import SettingsHook, SourceHook
# Local imports
from...io import IO


class FileSystemService:
    """
    Manage the file system for the controller.
    """

    SOURCES_DIR_NAME = "sources"
    SETTINGS_DIR_NAME = "settings"

    def __init__(self) -> None:
        # Objects
        self.io = IO()
        self.ws_dir_path = None

    ################################## MODIFIERS #############################

    def shutdown(self) -> None:
        # Remove the sources directory
        self.io.delete("{}/{}".format(self.ws_dir_path, self.SOURCES_DIR_NAME))

    def configure_from_workspace_path(self, ws_dir_path: str) -> bool:
        if not self.io.is_directory(ws_dir_path):
            return False
        self.ws_dir_path = ws_dir_path
        # Create a directory for sources and one for settings
        self.io.create_directory(
            "{}/{}".format(ws_dir_path, self.SOURCES_DIR_NAME))
        # Create a directory for settings profiles
        self.io.create_directory("{}/{}".format(
            ws_dir_path, self.SETTINGS_DIR_NAME))
        return True

    def generate_settings_hook(self, settings_profile_name: str) \
            -> SettingsHook:
        """
        Generate a settings hook for the specified settings profile name.
        Hook allows a settings profile to interact with the file system.
        A hook with the same name cannot be re-added.

        Args:
            settings_profile_name (str)

        Returns:
            (SettingsHook)
        """
        self._raise_configure_exception()
        try:
            return SettingsHook(
                settings_profile_name,
                "{}/{}".format(self.ws_dir_path, self.SETTINGS_DIR_NAME))
        except:
            pass

    def generate_source_hook(self, source_name: str, result_dir_path: str) \
            -> SourceHook:
        """
        Generate a hook for the specified source.
        The hook allows the source to interact with the file system.
        A hook with the same name cannot be re-added.

        Args:
            source_name (str)

        Returns:
            (SourceHook)
        """
        self._raise_configure_exception()
        try:
            return SourceHook("{}/{}".format(
                self.ws_dir_path, self.SOURCES_DIR_NAME,
            ), source_name, result_dir_path)
        except:
            pass

    ################################## GETTERS ###############################

    def is_workspace_configured(self):
        return self.io.is_directory(
            "{}/{}".format(self.ws_dir_path, self.SETTINGS_DIR_NAME)) and \
            self.io.is_directory(
            "{}/{}".format(self.ws_dir_path, self.SOURCES_DIR_NAME))

    ##########################  PRIVATE METHODS ###############################

    def _raise_configure_exception(self) -> None:
        """
        Raise an exception if the workspace is not configured.
        """
        if not self.is_workspace_configured():
            raise Exception("Workspace not configured")
