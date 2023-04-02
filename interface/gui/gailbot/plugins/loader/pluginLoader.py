import os 
from typing import Dict, List, Union, TypedDict, Tuple
from abc import ABC
from ..suite import PluginSuite
from gailbot.core.utils.logger import makelogger
from gailbot.core.utils.general import (
    filepaths_in_dir,
    get_name,
    get_extension,
    copy,
    read_toml,
    get_parent_path,
    is_directory,
)
from gailbot.core.utils.download import download_from_urls
from pydantic import BaseModel, ValidationError
from urllib.parse import urlparse

logger = makelogger("plugin_loader")

class PluginLoader(ABC):
    """ base class for plugin loader """
    def load(self, *args, **kwargs) -> List[PluginSuite]:
        raise NotImplementedError()