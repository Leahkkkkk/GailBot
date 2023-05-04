import os
import pip
from cryptography.fernet import Fernet
from typing import Dict, List, Union, TypedDict, Tuple
from dataclasses import dataclass
from .pluginLoader import PluginLoader
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
    delete,
)
from config_backend import PROJECT_ROOT
from gailbot.configs import PLUGIN_CONFIG
from pydantic import BaseModel, ValidationError


logger = makelogger("plugin directory loader")


class PluginDict(BaseModel):
    """dictionary type for individual plugin"""

    plugin_name: str
    dependencies: List[str]
    module_name: str
    rel_path: str


class ConfDict(TypedDict):
    """dictionary type for plugin suite configuration dictionary"""

    suite_name: str
    plugins: List[PluginDict]


class MetaData(BaseModel):
    Version: str
    Author: str


class ConfModel(BaseModel):
    """dictionary type for plugin suite configuration dictionary"""

    metadata: MetaData
    suite_name: str
    plugins: List[PluginDict]


class PluginDirectoryLoader(PluginLoader):
    """load the plugin suite from a directory that contains all source
    script implementing the plugins, and a toml file that stores
    configuration information to load the plugin
    """

    def __init__(
        self,
        suites_dir: str,
    ):
        """initialize a plugin directory loader

        Args:
            suites_dir (str): the path to the directory that stores all the
                              copies of plugins will be stored and managed
                              by plugin manager
        """
        self.suites_dir = suites_dir
        self.toml_loader = PluginTOMLLoader()

    def load(self, suite_dir_path: str) -> Union[PluginSuite, bool]:
        """load the plugin from a directory

        Args:
            suite_dir_path (str): path to the source directory that contains
                                  the entire plugin suite
        Returns:
            return a PluginSuite object that stores the loaded suite
            if the plugin can be successfully loaded, return false otherwise
        """
        if (not type(suite_dir_path) == str) or (not is_directory(suite_dir_path)):
            logger.info(suite_dir_path)
            logger.error("not a plugin")
            # check for invalid input
            return False

        suite_dir_name = get_name(suite_dir_path)
        logger.info(f"suite name is {suite_dir_name}, suite path is {suite_dir_path}")
        tgt_path = f"{self.suites_dir}/{get_name(suite_dir_path)}"

        config = None
        requirement = None
        official = None
        document = None
        format = None

        # search for the requirements and config file
        for root, dirs, files in os.walk(suite_dir_path):
            if PLUGIN_CONFIG.REQUIREMENT in files:
                requirement = os.path.join(root, PLUGIN_CONFIG.REQUIREMENT)
            if PLUGIN_CONFIG.CONFIG in files:
                config = os.path.join(root, PLUGIN_CONFIG.CONFIG)
            if PLUGIN_CONFIG.DOCUMENT in files:
                document = os.path.join(root, PLUGIN_CONFIG.DOCUMENT)
            if PLUGIN_CONFIG.OFFICIAL in files:
                official = os.path.join(root, PLUGIN_CONFIG.OFFICIAL)
            if PLUGIN_CONFIG.FORMAT in files:
                format = os.path.join(root, PLUGIN_CONFIG.FORMAT)
            if config and requirement and document and official and format:
                break

        if not config or not document or not format:
            return False

        # download required package
        try:
            if requirement:
                self.download_packages(requirement, PROJECT_ROOT)
        except Exception as e:
            logger.error(f"failed to download package", exc_info=e)
            return False

        # make a copy of the original plugin suite
        if not is_directory(tgt_path):
            copy(suite_dir_path, tgt_path)

        if is_directory(tgt_path) and self.suites_dir not in suite_dir_path:
            delete(tgt_path)
            copy(suite_dir_path, tgt_path)

        suite = self.toml_loader.load(config, suite_dir_name, self.suites_dir)

        if suite:
            # validate
            if self.validate_official(official):
                suite.set_to_official_suite()
            return [suite]
        else:
            delete(tgt_path)
            return False

    def download_packages(self, req_file, dest):
        """download packages listed under req_file to dest

        Args:
            req_file(str): a string that specifies the path to requirements.txt file
            dest (str): a string to the directory where the file will be downloaded
        """
        if hasattr(pip, "main"):
            pip.main(["install", "-t", str(dest), "-r", req_file])

    def validate_official(self, file):
        """given a file that stores the key, verify the key

        Args:
            file (str): path to the file

        Returns:
            bool: return true if the key matches with the official gailbot plugin
        """
        if not file:
            return False
        try:
            with open(file, "r") as f:
                key = f.read()
            fernet = Fernet(PLUGIN_CONFIG.OFFICIAL_ENKEY)

            decrypt = fernet.decrypt(key)

            if decrypt == PLUGIN_CONFIG.OFFICIAL_KEY:
                return True
            else:
                return False
        except Exception as e:
            logger.error(e, exc_info=e)
            return False


class PluginTOMLLoader(PluginLoader):
    """import all modules in the plugin, all plugin sources and dependencies
    are described in a configuration file in toml format
    """

    def __init__(self):
        self.dict_config_loader = PluginDictLoader()

    def load(
        self, conf_path: str, suite_name: str, suites_directory: str
    ) -> PluginSuite:
        """given the path to configuration file of one plugin suite, and
             the suites directory that stores all plugin suites ,
             import the plugin suite described in the configuration file

        Args:
            conf_path (str): a path to the configuration file
            suites_directory (str): a path to the directory that contain
                                    all plugin suites

        Returns:
            PluginSuite:
            return a PluginSuite object that stores the loaded suite
            if the plugin can be successfully loaded, return false otherwise
        """
        validated, conf = PluginTOMLLoader.validate_config(conf_path, suite_name)
        if validated:
            conf.update({"path": get_parent_path(conf_path)})
            return self.dict_config_loader.load(conf, suites_directory)
        else:
            logger.error(f"Error: {conf}")
            return False

    @staticmethod
    def validate_config(
        conf_path: str, suite_name: str
    ) -> Tuple[bool, Union[str, Dict]]:
        """
        validate if the plugin configuration file is in the correct format

        Args:
            conf_path (str): path to the configuration file
            suite_name (str): suite name

        Returns:
            Tuple(bool, Union[str, Dict]):
            for valid configuration, return True and dictionary that stores the
            toml file information;
            for invalid configuration file, return False and error message
        """
        if not type(conf_path) == str:
            return (False, "Invalid file path")
        if (not os.path.isfile(conf_path)) or (not get_extension(conf_path) == "toml"):
            return (False, "Invalid file path")
        dict_conf = read_toml(conf_path)
        try:
            ConfModel(**dict_conf)
        except ValidationError as e:
            logger.error(f"invalid scheme {e}")
            return (False, f"invalid scheme {e}")
        if dict_conf["suite_name"] == suite_name:
            return (True, dict_conf)
        else:
            logger.error(f"suite name is {suite_name}")
            return (False, "suite name must be the same as the folder name")


class PluginDictLoader(PluginLoader):
    """load a plugin suite from a dictionary that contains the configuration
    of all plugin dependencies and sources
    """

    def load(self, dict_conf: Dict, suites_directory: str) -> PluginSuite:
        if not type(dict_conf) == dict:
            return ""
        suite = PluginSuite(dict_conf, suites_directory)
        if suite.is_ready:
            return suite
        else:
            return False
