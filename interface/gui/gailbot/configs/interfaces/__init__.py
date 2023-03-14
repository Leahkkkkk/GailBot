# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-31 15:29:08
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-31 15:37:25

from ..confs.paths import PATH, CONFIG_ROOT, PROJECT_ROOT
from .core.engines.watson import load_watson_config
from .core.engines.google import load_google_config
from .core.engines.whisper import load_whisper_config
from .core.setting.defaults import load_default_config
from .core.util.logger import load_log_config
from .config.path_config import load_workspace_config, load_ws_root, store_ws_root
from .services import load_service_config, load_default_setting
from .config.path_config import TemporaryFolder, OutputFolder
import os

def watson_config_loader(): return load_watson_config(
    os.path.join(CONFIG_ROOT, PATH.watson))

def google_config_loader(): return load_google_config(
    os.path.join(CONFIG_ROOT, PATH.google))


def whisper_config_loader(): return load_whisper_config(
    os.path.join(CONFIG_ROOT, PATH.whisper)
)

def service_config_loader(): return load_service_config(
    os.path.join(CONFIG_ROOT, PATH.services)
)

def log_config_loader(): return load_log_config(
    os.path.join(CONFIG_ROOT, PATH.log)
)

def workspace_config_loader(user_root): return load_workspace_config(
    os.path.join(CONFIG_ROOT, PATH.paths_config), user_root
)

def default_setting_loader(): return load_default_setting(
    os.path.join(CONFIG_ROOT, PATH.default_setting)
)

def get_ws_root(): return load_ws_root(
    os.path.join(CONFIG_ROOT, PATH.ws_root)
)

def save_ws_root(user_root: str): return store_ws_root(
    os.path.join(CONFIG_ROOT, PATH.ws_root), user_root
)
