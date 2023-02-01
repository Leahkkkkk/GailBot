import logging
import os 
from datetime import date
from .general import make_dir, is_directory
""" TODO: confirm the log directory position """

ROOT_PATH = "./log_files"
log_directory = os.path.join(os.getcwd(), ROOT_PATH)
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
    formatter = logging.Formatter('%(asctime)s - %(funcName)s - %(lineno)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)
    return logger
