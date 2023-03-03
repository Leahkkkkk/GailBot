# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-31 15:29:08
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-31 15:37:25

from ..confs.paths import PATH, CONFIG_ROOT
from .core.engines.watson import load_watson_config
from .core.engines.google import load_google_config
from .core.engines.whisper import load_whisper_config
from .core.setting.defaults import load_default_config
from .core.util.logger import load_log_config
from .config.config import load_top_config
from .config.path_config import load_path_config
from .config.path_config import TemporaryFolder, OutputFolder
# from .services import load_file_extensions, load_conversation_payload, load_transdir_payload, load_result, load_interfaces, load_default_settings
import os

def watson_config_loader(): return load_watson_config(
    os.path.join(CONFIG_ROOT, PATH.watson))


def google_config_loader(): return load_google_config(
    os.path.join(CONFIG_ROOT, PATH.google))


def whisper_config_loader(): return load_whisper_config(
    os.path.join(CONFIG_ROOT, PATH.whisper)
)

def default_config_loader(): return load_default_config(
    os.path.join(CONFIG_ROOT, PATH.default))


def log_config_loader(): return load_log_config(
    os.path.join(CONFIG_ROOT, PATH.log))



def path_config_loader():
    return load_path_config(
        os.path.join(CONFIG_ROOT, PATH.paths_config),
        os.path.join(CONFIG_ROOT, PATH.root)
    )

# def file_extensions_loader():
#     return load_file_extensions(os.path.join(CONFIG_ROOT, PATH.services))
    
# def interface_loader():
#     return load_interfaces(os.path.join(CONFIG_ROOT, PATH.services))
