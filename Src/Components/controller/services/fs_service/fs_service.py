# Standard library imports
from typing import Dict, Any, List
# Local imports
from .....utils.manager import ObjectManager
from ....io import IO
from ....organizer import Settings
from .settings_hook import SettingsHook
from .source_hook import SourceHook
from .paths import Paths

class FileSystemService:

    def __init__(self) -> None:
        ## Objects
        self.io = IO()
        self.settings_hooks = ObjectManager()
        self.source_hooks = ObjectManager()
        self.paths = None

    ################################## MODIFIERS #############################

    def configure_from_workspace_path(self, ws_dir_path : str) -> bool:
        if not self.io.is_directory(ws_dir_path):
            return False
        self.paths = Paths(ws_dir_path)
        return self._initialize_workspace()

    def shutdown(self) -> None:
        if not self.is_workspace_configured():
            return
        # Cleanup all the source hooks.
        source_hooks = self.source_hooks.get_all_objects()
        for source_hook in source_hooks.values():
            source_hook : SourceHook
            source_hook.cleanup()
        # Delete the sources directory.
        self.io.delete(self.paths.get_sources_workspace_path())
        self.io.delete(self.paths.get_temporary_workspace_path())

    def generate_settings_hook(self, settings_profile_name : str) \
            -> SettingsHook:
        self._raise_configure_exception()
        if self.is_settings_hook(settings_profile_name):
            return
        hook = SettingsHook(
            settings_profile_name, self.paths.get_settings_workspace_path(),
            self.paths.get_settings_profile_extension())
        hook.register_listener(
            "cleanup",
            lambda _ : self.remove_settings_hook(settings_profile_name))
        self.settings_hooks.add_object(settings_profile_name,hook)
        return hook

    def generate_source_hook(self, source_name : str) -> SourceHook:
        self._raise_configure_exception()
        if self.is_source_hook(source_name):
            return
        # Create the new source directory.
        source_dir_path = self.paths.get_source_dir_path(source_name)
        if not self.io.create_directory(source_dir_path):
            return
        hook = SourceHook(source_dir_path)
        hook.register_listener(
            "cleanup",lambda _: self.remove_source_hook(source_name))
        self.source_hooks.add_object(source_name,hook)
        return hook

    def remove_source_hook(self, source_name : str) -> bool:
        # Delete the hook directory.
        source_hook : SourceHook = self.source_hooks.get_object(source_name)
        return self.io.delete(source_hook.get_path()) and \
                self.source_hooks.remove_object(source_name)

    def remove_settings_hook(self, settings_profile_name : str) -> bool:
        return self.settings_hooks.remove_object(settings_profile_name)

    def generate_source_result_directory(self, source_name : str,
            result_dir_path : str) -> str:
        if not self.io.is_directory(result_dir_path):
            return
        dir_path = "{}/{}".format(result_dir_path,source_name)
        self.io.create_directory(dir_path)
        return dir_path

    ################################## GETTERS ###############################

    def get_temporary_workspace_path(self) -> str:
        return self.paths.get_temporary_workspace_path()

    def is_workspace_configured(self) -> bool:
        return self.paths != None and \
            self.io.is_directory(self.paths.get_sources_workspace_path()) and \
            self.io.is_directory(self.paths.get_settings_workspace_path())
            # TODO: UNCOMMENT THIS.
            # self.io.is_file(self.paths.get_config_service_config_file_path())

    def is_settings_hook(self, settings_profile_name : str) -> bool:
        self._raise_configure_exception()
        return self.settings_hooks.is_object(settings_profile_name)

    def is_source_hook(self, source_name : str) -> bool:
        self._raise_configure_exception()
        return self.source_hooks.is_object(source_name)

    def get_settings_hook(self, settings_profile_name) -> SettingsHook:
        self._raise_configure_exception()
        return self.settings_hooks.get_object(settings_profile_name)

    def get_source_hook(self, source_name : str) -> SourceHook:
        self._raise_configure_exception()
        return self.source_hooks.get_object(source_name)

    def get_all_settings_hooks(self) -> Dict[str,SettingsHook]:
        self._raise_configure_exception()
        return self.settings_hooks.get_all_objects()

    def get_all_source_hooks(self) -> Dict[str,SourceHook]:
        self._raise_configure_exception()
        return self.source_hooks.get_all_objects()

    def get_source_hook_names(self) -> List[str]:
        self._raise_configure_exception()
        return self.source_hooks.get_object_names()

    def get_settings_hook_names(self) -> List[str]:
        self._raise_configure_exception()
        return self.settings_hooks.get_object_names()

    ## ConfigService

    def get_config_service_data_from_disk(self) -> Dict:
        self._raise_configure_exception()
        success, data = self.io.read(
            self.get_config_service_configuration_source())
        return {} if not success else data

    def get_config_service_configuration_source(self) -> str:
        self._raise_configure_exception()
        return self.paths.get_config_service_config_file_path()

    ##########################  PRIVATE METHODS ###############################



    def _raise_configure_exception(self) -> None:
        if not self.is_workspace_configured():
            raise Exception("Workspace not configured")

    def _initialize_workspace(self) -> bool:
        # TODO: UNCOMMENT THIS.
        # if not self.io.is_file(self.paths.get_config_service_config_file_path()):
        #     return False
        sources_ws_path = self.paths.get_sources_workspace_path()
        settings_ws_path = self.paths.get_settings_workspace_path()
        temporary_ws_path = self.paths.get_temporary_workspace_path()
        # Creating dirs
        if self.io.is_directory(sources_ws_path):
            self.io.delete(sources_ws_path)
        if not self.io.is_directory(sources_ws_path):
            if not self.io.create_directory(sources_ws_path):
                return False
        if self.io.is_directory(temporary_ws_path):
            self.io.delete(temporary_ws_path)
        self.io.create_directory(temporary_ws_path)
        if self.io.is_directory(settings_ws_path):
            # Creating settings profile from paths.
            _, file_paths = self.io.path_of_files_in_directory(
                settings_ws_path,[self.paths.get_settings_profile_extension()],
                False)
            for file_path in file_paths:
                self.generate_settings_hook(self.io.get_name(file_path))
        else:
            if not self.io.create_directory(settings_ws_path):
                return False
        return True






