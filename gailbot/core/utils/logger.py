import logging
import os 
from datetime import date
from .general import make_dir, is_directory
from gailbot.configs import log_config_loader, top_level_config_loader

TOP_LEVEL = top_level_config_loader()

LOG_CONFIG  = log_config_loader()
log_directory = os.path.join(TOP_LEVEL.root, TOP_LEVEL.workspace.log_files)
if not is_directory(log_directory):
    make_dir(log_directory)

def makelogger(filename:str):
    today = date.today()
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    # Create a file handler
    path = os.path.join(log_directory, f"{filename}-{today}.log")
    file_handler = logging.FileHandler(path)
    file_handler.setLevel(logging.INFO)

    # Create a formatter
    formatter = logging.Formatter(LOG_CONFIG.formatter)
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)
    return logger
