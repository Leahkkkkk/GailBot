from dataclasses import dataclass
import os
from typing import Union, List
from gailbot.configs import (
    path_config_loader, 
    save_ws_root, 
    service_config_loader,
    PROJECT_ROOT, 
    TemporaryFolder, 
    OutputFolder)
from gailbot.core.utils.general import (
    is_directory, 
    make_dir,
    delete, 
    paths_in_dir)
from gailbot.core.utils.logger import makelogger

CONFIG = service_config_loader()
TEMP = CONFIG.directory_name.temp_extension
OUTPUT = CONFIG.directory_name.output_extension
logger = makelogger("workspace")

@dataclass
class WorkspaceManager:
    """ store the path data of the workspace, provide utility function to 
        create temporary and output directories 
    """
    def __init__(self, user_root: str ) -> None:
        self.path_config         = path_config_loader(user_root)
        self.user_root:      str = user_root
        self.setting_src:    str = self.path_config.gailbot_data.setting_src
        self.plugin_src:     str = self.path_config.gailbot_data.plugin_src
        self.tempspace_root: str = self.path_config.tempspace_root
        self.log_root:    str = self.path_config.log_root
    
    def init_workspace(self):
        """
        initializing the workspace
        """
        for path in self.path_config.gailbot_data.__dict__.values():
            if not is_directory(path):
                make_dir(path, True)
                
        if not is_directory(self.path_config.tempspace_root):
                make_dir(self.path_config.tempspace_root, True)
        
        save_ws_root(self.user_root)
        
    def get_file_temp_space(self, name: str) -> Union[TemporaryFolder, bool]:
        """ given the file name, create a directory for the file
            to store temporary files created during the transcription process

        Args:
            name (str): name of the file 

        Returns:
            Union[TemporaryFolder, bool]: if the temporary folder is created 
            successfully, return a TemporaryFolder dataclass object that 
            stores the path of each subfolder under the temporary folder, 
            else return False
        """
        folder: TemporaryFolder = self.path_config.get_temp_space(name + TEMP) 
        try:
            for path in folder.__dict__.values(): 
                if not is_directory(path):
                    make_dir(path, True)
            return folder
        except Exception as e:
            logger.error(e)
            return False
        
    def get_output_space(self, outdir: str, name: str) -> Union[OutputFolder, bool]:
        """ given the file name, and the root path of the output, create a 
            directory for the file to store output files 

        Args:
            outdir (str): output path of the file 
            name (str): name of the file 

        Returns:
            Union[OutputFolder, bool]: if the output folder is created 
            successfully, return a OutputFolder dataclass object that 
            stores the path of each subfolder under the output folder, 
            else return False
        """
        folder: OutputFolder = self.path_config.get_output_space(outdir, name + OUTPUT)
        try:
            for path in folder.__dict__.values():
                if not is_directory(path):
                    make_dir(path, True)
            return folder
        except Exception as e:
            logger.error(e)
            return False
    
    
    def clear_temp_space(self, temp_space: Union[str, TemporaryFolder]):
        """clear the temporary space of a certain file

        Args:
            temp_space (Union[str, TemporaryFolder]): either a 
            Temporary folder object that stores the path to the temporary 
            directories, or the name of the original file that can be used 
            to identify its temporary folder

        Returns:
            _type_: _description_
        """
        try: 
            if isinstance(temp_space, TemporaryFolder):
                delete(temp_space.root)
            else:
                delete(self.path_config.get_temp_space(temp_space + TEMP).root)
                return True
        except Exception as e:
            logger.error(e)
            return False
        
    def clear_gb_temp_dir(self):
        """
        Clears the temporary workspace directory

        Returns:
            False if exception is raised
        """
        try:
            if is_directory(self.path_config.tempspace_root):
                delete(self.path_config.tempspace_root)
        except Exception as e:
            logger.error(e)
            return False
        
    def get_setting_file(self) -> List[str]:
        """ get the list of paths to the saved setting files

        Returns:
            List[str]: a list of paths to the saved setting files
        """
        try: 
            return paths_in_dir(self.path_config.gailbot_data.setting_src, ["toml"])
        except Exception as e:
            logger.error(e)
            return False 
    
    def clear_log(self) -> bool:
        """ clear the log files in the gailbot workspace folder

        Returns:
            bool: true if the deletion is successful, false otherwise 
        """
        try:
            if is_directory(self.path_config.log_root):
                delete(self.path_config.log_root)
            return True
        except Exception as e:
            logger.error(e)
            return False