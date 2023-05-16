from gailbot.configs import (
    log_config_loader, 
    google_config_loader, 
    watson_config_loader, 
    )
import logging
def test_config_file():
    WATSON_CONFIG = log_config_loader()
    WATSON_CONFIG = watson_config_loader()
    GOOGLE_CONFIG = google_config_loader()

