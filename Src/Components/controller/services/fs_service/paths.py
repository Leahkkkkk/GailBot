# Standard imports
# Local imports
from ....io import IO

class Paths:
    """
    Manage path names for the file system.
    """

    def __init__(self, workspace_dir_path : str) -> None:
        ## Vars.
        self.workspace_dir_path = workspace_dir_path
        self.source_ws_name = "sources"
        self.settings_ws_name = "settings_profiles"
        self.settings_profile_extension = "json"
        self.config_service_file_name = "config"
        self.config_service_file_extension = "json"
        ## Objects
        self.io = IO()

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

    def get_system_blackboard_configuration_path(self) -> str:
        """
        Path to the system blackboard configuration file, which must
        be named 'system_blackboard.json'
        """
        success, file_paths = self.io.path_of_files_in_directory(
            self.workspace_dir_path,['json'],True)
        if not success:
            return
        for path in file_paths:
            if self.io.get_name(path) == "system_blackboard" and \
                    self.io.get_file_extension(path)[1] == 'json':
                return path



