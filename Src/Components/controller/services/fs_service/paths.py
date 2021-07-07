# Standard imports

class Paths:
    """
    Manage path names for the file system.
    """

    def __init__(self, workspace_dir_path : str) -> None:
        self.workspace_dir_path = workspace_dir_path
        self.source_ws_name = "sources"
        self.settings_ws_name = "settings_profiles"
        self.temporary_workspace_name = "temporary_workspace"
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

    def get_temporary_workspace_path(self) -> str:
        """
        Obtain the path to the temporary workspace inside the workspace.

        Returns:
            (str): Temporary workspace path.
        """
        return "{}/{}".format(
            self.workspace_dir_path,self.temporary_workspace_name)

     ## Sources

    def get_sources_workspace_path(self) -> str:
        """
        Obtain the sources workspace path.

        Returns:
            (str): Path to the sources workspace directory.
        """
        return "{}/{}".format(self.workspace_dir_path,self.source_ws_name)

    def get_source_result_directory_path(self, source_name : str,
            result_dir_path : str) -> str:
        """
        Obtain the source result directory path for the given source.

        Args:
            source_name (str)
            result_dir_path (str): Parent directory path.
        """
        return "{}/{}".format(result_dir_path,source_name)

    def get_source_temporary_workspace_path(self, source_name : str) -> str:
        """
        Obtain the temporary workspace path for the specified source.

        Args:
            (source_name)

        Returns:
            (str): Temporary workspace path for the specified source.
        """
        return "{}/{}".format(self.get_temporary_workspace_path(),
            source_name)

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




