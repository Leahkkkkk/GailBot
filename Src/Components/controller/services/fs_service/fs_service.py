# Standard library imports
from typing import Dict, Any, List
# Local imports
from ....io import IO
from ....organizer import Settings

# Third party imports

class FileSystemService:

    def __init__(self) -> None:
        ## Variables
        self.ws_dir_path = None
        ## Objects
        self.io = IO()
        self.settings_file_extension = "json"
        self.settings_dir_name = "settings_profiles"
        self.config_service_file_extension = "json"
        self.config_service_file_name = "config"
        self.source_ws_name = "source_ws"

    ################################## MODIFIERS #############################

    def configure_from_workspace_path(self, ws_dir_path : str) -> bool:
        if self._initialize_workspace(ws_dir_path):
            self.ws_dir_path = ws_dir_path
            return True
        return False

    def shutdown(self) -> bool:
        # Delete the sources workspace
        return self.is_configured() and \
            self.io.delete(
                self._generate_sources_workspace_path(self.ws_dir_path))

    #### OrganizerService

    ## SettingsProfile

    def save_settings_profile_to_disk(self, settings_profile_name : str,
            settings : Settings) -> bool:
        if not self.is_configured():
            return False
        settings_profile_path = self._generate_settings_profile_path(
            settings_profile_name)

        return settings.save_to_file(
            lambda data: self.io.write(settings_profile_path,data,True))

    def load_saved_settings_profile_data_from_disk(self,
            settings_profile_name : str) -> Dict:
        if not self.is_configured():
            return
        path = self._generate_settings_profile_path(settings_profile_name)
        if not self.io.is_file(path):
            return
        success,data = self.io.read(path)
        if not success:
            return
        return data

    def load_all_settings_profiles_data_from_disk(self) -> Dict[str,Any]:
        if not self.is_configured():
            return
        data = dict()
        settings_dir_path = self._generate_settings_profile_dir_path(
            self.ws_dir_path)
        file_paths = self.io.path_of_files_in_directory(settings_dir_path,
            [self.settings_file_extension],False)[1]
        for file_path in file_paths:
            name = self.io.get_name(file_path)
            data[name] = self.load_saved_settings_profile_data_from_disk(name)
        return data

    def remove_settings_profile_from_disk(self,
            settings_profile_name : str) -> bool:
        if not self.is_configured():
            return False
        path = self._generate_settings_profile_path(settings_profile_name)
        return self.io.delete(path)

    ## Source

    def create_source_workspace_on_disk(self, source_name : str) -> bool:
        if not self.is_configured():
            return False
        path = self._generate_source_temporary_dir_path(source_name)
        if self.io.is_directory(path):
            return False
        self.io.create_directory(path)
        return True

    def cleanup_source_workspace_from_disk(self, source_name : str) -> bool:
        if not self.is_configured():
            return False
        path = self._generate_source_temporary_dir_path(source_name)
        return self.io.delete(path)

    ################################## GETTERS ###############################

    def is_configured(self) -> bool:
        return self.ws_dir_path != None and \
            self.io.is_directory(self.ws_dir_path) and \
            self._exists_config_service_configuration_file(self.ws_dir_path) and \
            self._exists_settings_profile_directory(self.ws_dir_path) and \
            self._exists_sources_workspace(self.ws_dir_path)

    def get_workspace_dir_path(self) -> str:
        return self.ws_dir_path

    ## ConfigService

    def get_config_service_data_from_disk(self) -> Dict:
        if not self.is_configured():
            return
        path = self._generate_config_service_config_file_path(self.ws_dir_path)
        success,data = self.io.read(path)
        if not success:
            return
        return data

    def get_config_service_configuration_source(self) -> str:
        if not self.is_configured():
            return None
        return self._generate_config_service_config_file_path(self.ws_dir_path)

    #### OrganizerService
    ## Source

    ## SettingsProfile

    def is_saved_settings_profile(self, settings_profile_name : str) -> bool:
        if not self.is_configured():
            return False
        path = self._generate_settings_profile_path(settings_profile_name)
        return self.io.is_file(path)

    def get_saved_settings_profile_location_on_disk(self,
            settings_profile_name : str) -> str:
        if not self.is_configured():
            return
        path = self._generate_settings_profile_path(settings_profile_name)
        return path if self.io.is_file(path) else ""

    def get_saved_settings_profile_names(self) -> List[str]:
        settings_dir_path = self._generate_settings_profile_dir_path(
            self.ws_dir_path)
        file_paths = self.io.path_of_files_in_directory(settings_dir_path,
            [self.settings_file_extension],False)[1]
        return [self.io.get_name(path) for path in file_paths]

    ## Source

    def get_source_workspace_names(self) -> List[str]:
        names = list()
        if not self.is_configured():
            return names
        source_ws_path = self._generate_sources_workspace_path(self.ws_dir_path)
        # TODO: Need to add a method in IO to get directory names.
        file_paths = self.io.path_of_files_in_directory(
            source_ws_path,["*"],False)[1]
        for path in file_paths:
            if self.io.is_directory(path):
                names.append(self.io.get_name(path))
        return names

    def get_source_workspace_location_on_disk(self, source_name : str) -> str:
        if not self.is_configured():
            return
        path = self._generate_source_temporary_dir_path(source_name)
        return path if self.io.is_directory(path) else ""

    ################################## SETTERS ###############################

    def _initialize_workspace(self, ws_dir_path : str) -> bool:
        if not self.io.is_directory(ws_dir_path):
            return False
        if not self._exists_config_service_configuration_file(ws_dir_path):
            return False

        self._initialize_settings_profile_directory(ws_dir_path)
        self._initialize_sources_workspace(ws_dir_path)
        return self._exists_settings_profile_directory(ws_dir_path) and \
            self._exists_sources_workspace(ws_dir_path)

    def _exists_config_service_configuration_file(self, ws_dir_path : str) \
            -> bool:
        return self.io.is_file(
            self._generate_config_service_config_file_path(ws_dir_path))

    def _exists_settings_profile_directory(self, ws_dir_path : str) -> bool:
        return self.io.is_directory(
            self._generate_settings_profile_dir_path(ws_dir_path))

    def _exists_sources_workspace(self, ws_dir_path : str) -> bool:
        return self.io.is_directory(
            self._generate_sources_workspace_path(ws_dir_path))

    def _initialize_settings_profile_directory(self, ws_dir_path : str) -> bool:
        path = self._generate_settings_profile_dir_path(ws_dir_path)
        if self._exists_settings_profile_directory(path):
            return False
        return self.io.create_directory(path)

    def _initialize_sources_workspace(self, ws_dir_path : str) -> bool:
        path = self._generate_sources_workspace_path(ws_dir_path)
        if self._exists_sources_workspace(path):
            return False
        return self.io.create_directory(path)

    def _generate_config_service_config_file_path(self, ws_dir_path : str) \
            -> str:
        return "{}/{}.{}".format(ws_dir_path,
            self.config_service_file_name,self.config_service_file_extension)

    def _generate_settings_profile_dir_path(self, ws_dir_path : str) -> str:
        return "{}/{}".format(ws_dir_path,self.settings_dir_name)

    def _generate_sources_workspace_path(self, ws_dir_path : str) -> str:
        return "{}/{}".format(ws_dir_path, self.source_ws_name)

    def _generate_settings_profile_path(self, settings_profile_name : str) \
            -> str:
        if not self.is_configured():
            raise Exception("Not configured")
        return "{}/{}/{}.{}".format(
            self.ws_dir_path,self.settings_dir_name,settings_profile_name,
            self.settings_file_extension)

    def _generate_source_temporary_dir_path(self, source_name : str) -> str:
        if not self.is_configured():
            raise Exception("Not configured")
        return "{}/{}/{}".format(self.ws_dir_path,self.source_ws_name,
            source_name)









