import logging
import os 
from datetime import date
from pathlib import Path
from gailbot.configs import PROJECT_ROOT, log_config_loader, get_user_root, path_config_loader
from gailbot.core.utils.general import is_directory, make_dir, copy_dir_files, delete
import logging

LOG_CONFIG  = log_config_loader()
logging.info(get_user_root())

log_restored = False  # a global variable to check if there exists a temporary 
                      # log file in the project folder that was not moved 
                      # to the user's work space , set to true once it the log folder
                      # is moved 

def makelogger(logger_name:str):
    """ create a logger that can be identified by logger_name, and the logger's
        message will be stored into its own individual file inside the backend    
        folder
        
    Args:
        logger_name (str): the name of lof files

    Returns:
        logger: the logger
    """
    # get the all existing log handler 
    root_logger = logging.getLogger()
    handlers = root_logger.handlers 
    
    # get the named_log handler
    logger = logging.getLogger(logger_name)
    for handler in handlers:
        logger.addHandler(handler)
   
    logger.setLevel(logging.DEBUG)
    
    # get the root of the log file
    # if the toml file that stores the user's root does not exist, 
    # first store the log file in a temporary gailbot folder in the same level 
    # as the project root, which will be copied over to the permanent gailbot 
    # workspace 
    
    perm_log_space = get_user_root()
    temp_log_space = os.path.join(PROJECT_ROOT, LOG_CONFIG.temp_dir)
    logging.info(f"permenant_log_space is {perm_log_space}")
    logging.info(f"temporary_log_space is {perm_log_space}")
    if perm_log_space: 
        log_root = path_config_loader(perm_log_space).gailbot_data.logfiles 
        # if exists permanent log space, check if there is an temporary log 
        # space that has not been moved to the permanent log space
        global log_restored
        if not log_restored:
            if is_directory(temp_log_space): 
                copy_dir_files(temp_log_space, log_root)
                delete(temp_log_space)
            log_restored = True
    else: 
        log_root = temp_log_space
        
    if not is_directory(log_root):
        make_dir(log_root)
    
    # each backend log files one each date will be stored in a separate folder
    today = date.today()
    date_log_dir = os.path.join(log_root, f"{LOG_CONFIG.sub_dir_prefix}-{today}")
    make_dir(date_log_dir)
    path = os.path.join(date_log_dir, f"GailBot-{logger_name}-{today}.log")
    formatter = logging.Formatter(LOG_CONFIG.formatter)
    file_handler = logging.FileHandler(path)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger

