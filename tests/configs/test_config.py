from gailbot.configs import (
    log_config_loader, 
    top_level_config_loader, 
    google_config_loader, 
    watson_config_loader, 
    default_config_loader, 
    path_config_loader)

def test_config_file():
    WATSON_CONFIG = log_config_loader()
    TOP_CONFIG = top_level_config_loader()
    GOOGLE_CONFIG = top_level_config_loader()
    WATSON_CONFIG = watson_config_loader()
    DEFAULT_CONFIG = default_config_loader()
    GOOGLE_CONFIG = google_config_loader()

def test_path_config():
    PATH_CONFIG = path_config_loader()
    print(PATH_CONFIG.root)
    print(PATH_CONFIG.gailbot_data)
    print(PATH_CONFIG.log_dir)
    
    temp_workspace = PATH_CONFIG.get_temp_space("temp")
    print(temp_workspace.transcribe_ws)