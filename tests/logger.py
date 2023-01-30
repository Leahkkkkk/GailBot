import logging

def makelogger(filename:str):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    # Create a file handler
    file_handler = logging.FileHandler(f'tests/log/{filename}.log')
    file_handler.setLevel(logging.INFO)

    # Create a formatter
    formatter = logging.Formatter('%(asctime)s - %(funcName)s - %(lineno)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)
    return logger