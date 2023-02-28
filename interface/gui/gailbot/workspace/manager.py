from gailbot.configs import path_config_loader, TemporaryFolder, OutputFolder
from typing import Union, List, Dict, Any
from gailbot.core.utils.general import is_directory, make_dir, delete, paths_in_dir, subdirs_in_dir
from gailbot.core.utils.logger import makelogger
from dataclasses import dataclass

PATH_CONFIG = path_config_loader()
# FILE_CONFIG = file_extensions_loader()

TEMP = "_gb_temp"
OUTPUT = "_gb_output"
logger = makelogger("workspace")

@dataclass
class WorkspaceManager:
    """ store the path data of the workspace, provide utility function to 
        create temporary and output directories 
    """
    setting_src: str    = PATH_CONFIG.gailbot_data.setting_src
    log_file_space: str = PATH_CONFIG.gailbot_data.logfiles
    plugin_src: str     = PATH_CONFIG.gailbot_data.plugin_src
    tempspace_root: str = PATH_CONFIG.tempspace_root
    
    @staticmethod 
    def init_workspace():
        """
            initializing the workspace
        """
        for path in PATH_CONFIG.gailbot_data.__dict__.values():
            if not is_directory(path):
                make_dir(path, True)
        if not is_directory(PATH_CONFIG.tempspace_root):
                make_dir(PATH_CONFIG.tempspace_root, True)

    @staticmethod
    def get_file_temp_space(name: str) -> Union[TemporaryFolder, bool]:
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
        folder: TemporaryFolder = PATH_CONFIG.get_temp_space(name + TEMP) 
        try:
            for path in folder.__dict__.values(): 
                if not is_directory(path):
                    make_dir(path, True)
            return folder
        except Exception as e:
            logger.error(e)
            return False
        
    @staticmethod
    def get_output_space(outdir: str, name: str) -> Union[OutputFolder, bool]:
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
        folder: OutputFolder = PATH_CONFIG.get_output_space(outdir, name + OUTPUT)
        try:
            for path in folder.__dict__.values():
                if not is_directory(path):
                    make_dir(path, True)
            return folder
        except Exception as e:
            logger.error(e)
            return False
    
    
    @staticmethod
    def clear_temp_space(temp_space: Union[str, TemporaryFolder]):
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
                delete(PATH_CONFIG.get_temp_space(temp_space + TEMP).root)
                return True
        except Exception as e:
            logger.error(e)
            return False
        
    @staticmethod
    def clear_gb_temp_dir():
        try:
            if is_directory(PATH_CONFIG.tempspace_root):
                delete(PATH_CONFIG.tempspace_root)
        except Exception as e:
            logger.error(e)
            return False
        
    @staticmethod
    def get_setting_file() -> List[str]:
        """ get the list of paths to the saved setting files

        Returns:
            List[str]: a list of paths to the saved setting files
        """
        try: 
            return paths_in_dir(PATH_CONFIG.gailbot_data.setting_src, ["toml"])
        except Exception as e:
            logger.error(e)
            return False 
    
    @staticmethod
    def clear_log() -> bool:
        """ clear the log files in the gailbot workspace folder

        Returns:
            bool: true if the deletion is successful, false otherwise 
        """
        try:
            if is_directory(PATH_CONFIG.gailbot_data.logfiles):
                delete(PATH_CONFIG.gailbot_data.logfiles)
            return True
        except Exception as e:
            logger.error(e)
            return False