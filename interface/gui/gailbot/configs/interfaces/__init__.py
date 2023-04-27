# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-31 15:29:08
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-31 15:37:25

import os
import userpaths
from ..confs.paths import PATH, CONFIG_ROOT, PROJECT_ROOT
from .core.engines.watson import load_watson_config
from .core.engines.google import load_google_config
from .core.engines.whisper import load_whisper_config
from .core.setting.defaults import load_default_config
from .core.util.logger import load_log_config
from .config.ws_config import load_workspace_config
from .plugin import PLUGIN_CONFIG, load_valid_structure
from .services import load_service_config, load_default_setting
from .config.ws_config import TemporaryFolder, OutputFolder

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

def workspace_config_loader(): return load_workspace_config(
    os.path.join(CONFIG_ROOT, PATH.paths_config), get_ws_root()
)

def default_setting_loader(): return load_default_setting(
    os.path.join(CONFIG_ROOT, PATH.default_setting)
)

def get_ws_root(): return os.path.join(
    userpaths.get_profile(), "GailBot/Backend"
)

def get_plugin_structure_config():
    return load_valid_structure(os.path.join(CONFIG_ROOT, PATH.valid_plugin))

def get_format_md_path():
    return os.path.join(CONFIG_ROOT, PATH.format_md) 