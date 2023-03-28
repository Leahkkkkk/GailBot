import os 
from datetime import date
from pathlib import Path
import logging
import userpaths
from gailbot.configs import  log_config_loader 

LOG_CONFIG  = log_config_loader()

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
    # each backend log files one each date will be stored in a separate folder
    today = date.today()
    date_log_dir = os.path.join(
        userpaths.get_profile(), 
        LOG_CONFIG.log_dir, 
        f"{LOG_CONFIG.sub_dir_prefix}-{today}")
    if not Path(date_log_dir).is_dir():
        os.makedirs(date_log_dir)
    path = os.path.join(date_log_dir, f"GailBot-{logger_name}-{today}.log")
    formatter = logging.Formatter(LOG_CONFIG.formatter)
    file_handler = logging.FileHandler(path)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger

