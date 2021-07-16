# Standard imports

class Paths:
    """
    Manage path names for the file system.
    """

    def __init__(self, workspace_dir_path : str) -> None:
        self.workspace_dir_path = workspace_dir_path
        self.source_ws_name = "sources"
        self.settings_ws_name = "settings_profiles"
        self.settings_profile_extension = "json"
        self.config_service_file_name = "config"
        self.config_service_file_extension = "json"

    ################################## GETTERS ###############################

    ## General

    def get_workspace_path(self) -> str:
        """
        Obtain the path to the workspace.

        Returns:
            (str): Path to the workspace.
        """
        return self.workspace_dir_path

     ## Sources

    def get_sources_workspace_path(self) -> str:
        """
        Obtain the sources workspace path.

        Returns:
            (str): Path to the sources workspace directory.
        """
        return "{}/{}".format(self.workspace_dir_path,self.source_ws_name)

    ## Settings

    def get_settings_workspace_path(self) -> str:
        """
        Obtain the settings workspace path.

        Returns:
            (str): Settings workspace path.
        """
        return "{}/{}".format(self.workspace_dir_path,self.settings_ws_name)

    def get_settings_profile_extension(self) -> str:
        """
        Obtain the extension used by settings profile files.

        Returns:
            (str): Extension used by settings profiles files.
        """
        return self.settings_profile_extension

    ## Config service.

    def get_config_service_config_file_path(self) -> str:
        """
        Obtain the expected path for the config service configuration file.

        Returns:
            (str): config service configuration file path.
        """
        return "{}/{}.{}".format(
            self.workspace_dir_path,self.config_service_file_name,
            self.config_service_file_extension)




