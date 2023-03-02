import logging
import shutil
import os 
from datetime import date
from pathlib import Path
from gailbot.configs import log_config_loader, top_level_config_loader, path_config_loader

log_directory = path_config_loader().gailbot_data.logfiles
LOG_CONFIG  = log_config_loader()

def is_directory(dir_path: str) -> bool:
    """
    Determine if the given path is a directory.
    """
    try:
        return Path(dir_path).is_dir()
    except Exception as e:
        return False 
    
if not is_directory(log_directory):
    os.makedirs(log_directory, exist_ok=True)

def makelogger(filename:str):
    today = date.today()
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    # Create a file handler
    path = os.path.join(log_directory, f"{filename}-{today}.log")
    file_handler = logging.FileHandler(path)
    file_handler.setLevel(logging.DEBUG)

    # Create a formatter
    formatter = logging.Formatter(LOG_CONFIG.formatter)
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)
    logger = logging.LoggerAdapter(logger, {"source": "Backend"})
    return logger
