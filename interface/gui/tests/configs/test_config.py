from gailbot.configs import (
    log_config_loader, 
    google_config_loader, 
    watson_config_loader, 
    default_config_loader, 
    path_config_loader)
import logging
def test_config_file():
    WATSON_CONFIG = log_config_loader()
    WATSON_CONFIG = watson_config_loader()
    DEFAULT_CONFIG = default_config_loader()
    GOOGLE_CONFIG = google_config_loader()

def test_path_config():
    PATH_CONFIG = path_config_loader()
    print(PATH_CONFIG._user_root)
    print(PATH_CONFIG.gailbot_data)
    logging.info(PATH_CONFIG.workspace_root)
    logging.info(PATH_CONFIG.tempspace_root)
    logging.info(PATH_CONFIG.gailbot_data.root)
    logging.info(PATH_CONFIG.gailbot_data.setting_src)
    logging.info(PATH_CONFIG.gailbot_data.plugin_src)
    logging.info(PATH_CONFIG.gailbot_data.logfiles)
    logging.info(PATH_CONFIG.get_temp_space("test"))
    logging.info(PATH_CONFIG.get_output_space("test_out/path/to/output", "test")) 
    temp_workspace = PATH_CONFIG.get_temp_space("test")
    output = PATH_CONFIG.get_output_space("test_output", "test")
    logging.info(temp_workspace.transcribe_ws)
    logging.info(output.__dict__)