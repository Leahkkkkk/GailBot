

class Paths:

    def __init__(self, workspace_dir_path : str) -> None:
        self.workspace_dir_path = workspace_dir_path
        self.source_ws_name = "sources"
        self.settings_ws_name = "settings_profiles"
        self.temporary_workspace_name = "temporary_workspace"
        self.settings_profile_extension = "json"
        self.config_service_file_name = "config"
        self.config_service_file_extension = "json"

    ################################## GETTERS ###############################

    def get_workspace_path(self) -> str:
        return self.workspace_dir_path

    def get_sources_workspace_path(self) -> str:
        return "{}/{}".format(self.workspace_dir_path,self.source_ws_name)

    def get_source_dir_path(self, source_name : str) -> str:
        return "{}/{}".format(self.get_sources_workspace_path(),source_name)

    def get_settings_workspace_path(self) -> str:
        return "{}/{}".format(self.workspace_dir_path,self.settings_ws_name)

    def get_temporary_workspace_path(self) -> str:
        return "{}/{}".format(
            self.workspace_dir_path,self.temporary_workspace_name)

    def get_settings_profile_extension(self) -> str:
        return self.settings_profile_extension

    def get_config_service_config_file_path(self) -> str:
        return "{}/{}.{}".format(
            self.workspace_dir_path,self.config_service_file_name,
            self.config_service_file_extension)




