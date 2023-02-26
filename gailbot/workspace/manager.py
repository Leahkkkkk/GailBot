from gailbot.configs import path_config_loader, TemporaryFolder, OutputFolder, file_extensions_loader
from typing import Union, List, Dict, Any
from gailbot.core.utils.general import is_directory, make_dir, delete, paths_in_dir, subdirs_in_dir
from gailbot.core.utils.logger import makelogger
from dataclasses import dataclass

PATH_CONFIG = path_config_loader()
FILE_CONFIG = file_extensions_loader()

TEMP = FILE_CONFIG.temp
OUTPUT = FILE_CONFIG.output
logger = makelogger("workspace")

@dataclass
class WorkspaceManager:
    setting_src: str    = PATH_CONFIG.gailbot_data.setting_src
    log_file_space: str = PATH_CONFIG.gailbot_data.logfiles
    plugin_src: str     = PATH_CONFIG.gailbot_data.plugin_src
    tempspace_root: str = PATH_CONFIG.tempspace_root
    
    @staticmethod 
    def init_workspace():
        for path in PATH_CONFIG.gailbot_data.__dict__.values():
            if not is_directory(path):
                make_dir(path, True)
        if not is_directory(PATH_CONFIG.tempspace_root):
                make_dir(PATH_CONFIG.tempspace_root, True)

    @staticmethod
    def get_file_temp_space(name: str) -> Union[TemporaryFolder, bool]:
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
    def get_setting_file() -> List[str]:
       try: 
           return paths_in_dir(PATH_CONFIG.gailbot_data.setting_src, ["toml"])
       except Exception as e:
           logger.error(e)
           return False 
    
    @staticmethod
    def clear_log() -> bool:
        try:
            if is_directory(PATH_CONFIG.gailbot_data.logfiles):
                delete(PATH_CONFIG.gailbot_data.logfiles)
            return True
        except Exception as e:
            logger.error(e)
            return False