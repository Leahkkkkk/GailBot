# Standard library imports
from typing import Dict, List
# Local imports
from .....utils.manager import ObjectManager
from ....io import IO
from .settings_hook import SettingsHook
from .source_hook import SourceHook
from .paths import Paths

class FileSystemService:
    """
    Manage the file system for the controller.
    """

    def __init__(self) -> None:
        ## Objects
        self.io = IO()
        self.settings_hooks = ObjectManager()
        self.source_hooks = ObjectManager()
        self.paths = None

    ################################## MODIFIERS #############################

    def shutdown(self) -> None:
        """
        Properly shutdown the file system.
        """
        if not self.is_workspace_configured():
            return
        # Cleanup all the source hooks.
        source_hooks = self.source_hooks.get_all_objects()
        for source_hook in source_hooks.values():
            source_hook : SourceHook
            source_hook.cleanup()
            source_hook.destroy()
        # Delete the sources directory.
        self.io.delete(self.paths.get_sources_workspace_path())

    def configure_from_workspace_path(self, ws_dir_path : str) -> bool:
        """
        Configure the workspace using the specified workspace directory
        path.
        THe directory must contain the blackboard configuration file.

        Args:
            ws_dir_path (str): Path to the workspace directory.

        Returns:
            (bool): True if successful, False otherwise.
        """
        if not self.io.is_directory(ws_dir_path):
            return False
        self.paths = Paths(ws_dir_path)
        return self._initialize_workspace()

    def generate_settings_hook(self, settings_profile_name : str) \
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
        if self.is_settings_hook(settings_profile_name):
            return
        try:
            hook = SettingsHook(
                settings_profile_name, self.paths.get_settings_workspace_path(),
                self.paths.get_settings_profile_extension())
            self.settings_hooks.add_object(settings_profile_name,hook)
            return hook
        except:
            pass

    def generate_source_hook(self, source_name : str, result_dir_path : str) \
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
        if self.is_source_hook(source_name):
            return
        # Create the new source directory.
        parent_dir_path = self.paths.get_sources_workspace_path()
        try:
            hook = SourceHook(parent_dir_path, source_name, result_dir_path)
            self.source_hooks.add_object(source_name,hook)
            return hook
        except:
            pass

    def remove_source_hook(self, source_name : str) -> bool:
        """
        Remove the given source hook if it exists.

        Args:
            source_name (str): Name of the source.

        Returns:
            (bool): True if successfully removed, False otherwise.
        """
        if not self.source_hooks.is_object(source_name):
            return False
        # Delete the hook directory.
        source_hook : SourceHook = self.source_hooks.get_object(source_name)
        source_hook.cleanup()
        del source_hook
        return self.source_hooks.remove_object(source_name)

    def remove_settings_hook(self, settings_profile_name : str) -> bool:
        """
        Remove the given source hook if it exists.

        Args:
            settings_profile_name (str): Name of the profile.

        Returns:
            (bool): True if successfully removed, False otherwise.
        """
        if not self.settings_hooks.is_object(settings_profile_name):
            return False
        hook : SettingsHook = self.settings_hooks.get_object(
            settings_profile_name)
        hook.cleanup()
        del hook
        return self.settings_hooks.remove_object(settings_profile_name)

    ################################## GETTERS ###############################

    def is_workspace_configured(self) -> bool:
        """
        Determine if the workspace is configured.

        Returns:
            (bool): True if configured, False otherwise.
        """
        return self.paths != None and \
            self.io.is_directory(self.paths.get_sources_workspace_path()) and \
            self.io.is_directory(self.paths.get_settings_workspace_path())
            # TODO: UNCOMMENT THIS TO CHECK FOR BLACKBOARD CONFIG FILE.
            # self.io.is_file(self.paths.get_config_service_config_file_path())

    def is_settings_hook(self, settings_profile_name : str) -> bool:
        """
        Determine if the settings hook exists.

        Args:
            settings_profile_name (str)

        Returns:
            (bool): True if hook exists, False otherwise.
        """
        self._raise_configure_exception()
        return self.settings_hooks.is_object(settings_profile_name)

    def is_source_hook(self, source_name : str) -> bool:
        """
        Determine if source hook exists.

        Args:
            source_name (str)

        Returns:
            (bool): True if hook exists, False otherwise.
        """
        self._raise_configure_exception()
        return self.source_hooks.is_object(source_name)

    def get_settings_hook(self, settings_profile_name) -> SettingsHook:
        """
        Obtain the settings hook if it exists.

        Args:
            settings_profile_name (str)

        Returns:
            (SettingsHook)
        """
        self._raise_configure_exception()
        return self.settings_hooks.get_object(settings_profile_name)

    def get_source_hook(self, source_name : str) -> SourceHook:
        """
        Obtain the source hook if it exists.

        Args:
            source_name (str)

        Returns:
            (SourceHook)
        """
        self._raise_configure_exception()
        return self.source_hooks.get_object(source_name)

    def get_all_settings_hooks(self) -> Dict[str,SettingsHook]:
        """
        Obtain a mapping from settings names to their Hooks.

        Returns:
            (Dict[str,SettingsHook])
        """
        self._raise_configure_exception()
        return self.settings_hooks.get_all_objects()

    def get_all_source_hooks(self) -> Dict[str,SourceHook]:
        """
        Obtain a mapping from all sources to their hooks.

        Returns:
            (Dict[str,SourceHook])
        """
        self._raise_configure_exception()
        return self.source_hooks.get_all_objects()

    def get_source_hook_names(self) -> List[str]:
        """
        Obtain the names of all source hooks.

        Returns:
            (List[str])
        """
        self._raise_configure_exception()
        return self.source_hooks.get_object_names()

    def get_settings_hook_names(self) -> List[str]:
        """
        Obtain the names of all settings hooks.

        Returns:
            (List[str])
        """
        self._raise_configure_exception()
        return self.settings_hooks.get_object_names()

    ## ConfigService

    def get_config_service_data_from_disk(self) -> Dict:
        """
        Obtain configuration service data from disk.

        Returns:
            (Dict)
        """
        self._raise_configure_exception()
        success, data = self.io.read(
            self.get_config_service_configuration_source())
        return {} if not success else data

    def get_config_service_configuration_path(self) -> str:
        """
        Obtain the path of the configuration service config file.

        Returns:
            (str): Path of the configuration file.
        """
        self._raise_configure_exception()
        return self.paths.get_config_service_config_file_path()

    ##########################  PRIVATE METHODS ###############################

    def _raise_configure_exception(self) -> None:
        """
        Raise an exception if the workspace is not configured.
        """
        if not self.is_workspace_configured():
            raise Exception("Workspace not configured")

    def _initialize_workspace(self) -> bool:
        """
        Initialize the workspace.
        """
        return self._initialize_configuration_file() and \
            self._initialize_sources_workspace() and \
            self._initialize_settings_workspace()

    # TODO: Change this to accommodate file.
    def _initialize_configuration_file(self) -> bool:
        """
        Initialize the configuration file.
        """
        return True

    def _initialize_sources_workspace(self) -> bool:
        """
        Initialize the sources workspace directory.
        """
        sources_ws_path = self.paths.get_sources_workspace_path()
        self.io.delete(sources_ws_path)
        return self.io.create_directory(sources_ws_path)

    def _initialize_settings_workspace(self) -> bool:
        """
        Initialize the settings workspace directory and load any existing
        settings profiles.
        """
        settings_ws_path = self.paths.get_settings_workspace_path()
        if self.io.is_directory(settings_ws_path):
             # Creating settings profile from paths.
            _, file_paths = self.io.path_of_files_in_directory(
                settings_ws_path,[self.paths.get_settings_profile_extension()],
                False)
            return all([self.generate_settings_hook(self.io.get_name(file_path))\
                    for file_path in file_paths])
        return self.io.create_directory(settings_ws_path)
