import os
import re
import boto3
from botocore.exceptions import ParamValidationError
from cryptography.fernet import Fernet
from typing import Dict, List, Union, TypedDict, Tuple
from abc import ABC
from .directoryloader import PluginDirectoryLoader
from .pluginLoader import PluginLoader
from ..suite import PluginSuite
from gailbot.core.utils.logger import makelogger
from gailbot.core.utils.general import get_extension, read_toml, delete
from gailbot.configs import PLUGIN_CONFIG
from gailbot.core.utils.download import download_from_urls, is_internet_connected
from urllib.parse import urlparse
from urllib import request


logger = makelogger("url_loader")


class UrlLoader(ABC):
    """base class for loading plugin from url"""

    def __init__(self, download_dir, suites_dir) -> None:
        self.download_dir = download_dir
        self.suites_dir = suites_dir
        self.dir_loader = PluginDirectoryLoader(suites_dir)
        super().__init__()

    def is_supported_url(self, url: str) -> bool:
        """
        check if the url is supported
        """
        raise NotImplementedError

    def load(self, url: str) -> List[PluginSuite]:
        """load the source from the url"""
        raise NotImplementedError


class PluginURLLoader(PluginLoader):
    """
    plugin loader to download and load plugin suite from url,
    the loader can currently recognize and download plugin suite from
    github
    """

    def __init__(self, download_dir: str, suites_dir: str) -> None:
        super().__init__()
        self.download_dir = download_dir

        self.url_loaders: List[UrlLoader] = [
            GitHubURLLoader(download_dir, suites_dir),
            S3ZipLoader(download_dir, suites_dir),
            S3BucketLoader(download_dir, suites_dir),
        ]

    @property
    def supported_url_source(self):
        """return a list of supported url downloading source"""
        return ["github", "amazon s3"]

    @staticmethod
    def is_valid_url(self, url: str) -> bool:
        """
        check if the url string is valid

        Args:
            url (str): a string that represent the url

        Returns:
            bool: true if the string is valid url false otherwise
        """
        for loader in self.url_loaders:
            if loader.is_supported_url(url):
                return True

        return False

    def load(self, url: str) -> Union[PluginSuite, bool]:
        """
        load the plugin suite from the url if the url is supported by the
        list of the loader available,

        Args:
            url (str): url string

        Returns:
            PluginSuite: loaded plugin suite object if the url is supported
            Bool: return false if the url is not supported by current url loader
        """
        if not is_internet_connected():
            return False
        for loader in self.url_loaders:
            suites = loader.load(url)
            if isinstance(suites, List):
                return suites
        return False


class GitHubURLLoader(UrlLoader):
    """load plugin from an url source"""

    def __init__(self, download_dir, suites_dir) -> None:
        """initialize the plugin loader

        Args:
            download_dir (str): path to where the plugin suite will be downloaded
            suites_dir (str): path to where the plugin will be stored after
                              download
        """
        super().__init__(download_dir, suites_dir)

    def is_supported_url(self, url: str) -> bool:
        """given a url, returns true if the url is supported by the
             github loader

        Args:
            url (str): the url string
        """
        parsed = urlparse(url)
        if parsed.scheme == "https" and parsed.netloc == "github.com":
            return True
        else:
            return False

    def load(self, url: str) -> List[PluginSuite]:
        """download the plugin from a given url and stored a copy of the
            plugins in the suites directory

        Args:
            url (str): url for downloading the suite
            suites_directory  (str): path to where a copy of the plugin suite
                                    will be store

        Returns:
            PluginSuite: return a PluginSuite object that stores the loaded suite
        """
        # check if the type is valid
        if not self.is_supported_url(url):
            return False

        download_path = download_from_urls(
            urls=[url], download_dir=self.download_dir, unzip=True
        )[0]

        # get the suite name from the toml file
        for root, dirs, files in os.walk(download_path):
            if PLUGIN_CONFIG.CONFIG in files:
                config = os.path.join(root, PLUGIN_CONFIG.CONFIG)
                suite_name = read_toml(config)["suite_name"]
                break

        # get the suite directory
        for dirpath, dirnames, filename in os.walk(download_path):
            if suite_name in dirnames:
                suite_path = os.path.join(dirpath, suite_name)
                logger.info(f"the directory path is {suite_path}")
                break

        # Move to the suites dir.
        suites = self.dir_loader.load(suite_path)
        delete(download_path)
        return suites


class S3ZipLoader(UrlLoader):
    """load plugin from an url source"""

    def __init__(self, download_dir, suites_dir) -> None:
        """initialize the plugin loader

        Args:
            download_dir (str): path to where the plugin suite will be downloaded
            suites_dir (str): path to where the plugin will be stored after
                              download
        """
        super().__init__(download_dir, suites_dir)

    def is_supported_url(self, url: str) -> bool:
        """given a url, returns true if the url is supported by the
             github loader

        Args:
            url (str): the url string
        """
        regex = r"^https?://[a-zA-Z0-9.-]+\.s3\.[a-z]{2}-[a-z]+-\d{1,2}\.amazonaws\.com/.*\.zip$"
        match = re.match(regex, url)
        return bool(match)

    def load(self, url: str) -> PluginSuite:
        """download the plugin from a given url and stored a copy of the
            plugins in the suites directory

        Args:
            url (str): url for downloading the suite
            suites_directory  (str): path to where a copy of the plugin suite
                                    will be store

        Returns:
            PluginSuite: return a PluginSuite object that stores the loaded suite
        """
        # check if the type is valid
        if not self.is_supported_url(url):
            logger.info(f"url is not a supported url")
            return False

        download_path = download_from_urls(
            urls=[url], download_dir=self.download_dir, unzip=True
        )[0]
        logger.info(f"file is downloaded to {download_path}")
        # get the suite name from the toml file
        for root, dirs, files in os.walk(download_path):
            if PLUGIN_CONFIG.CONFIG in files:
                config = os.path.join(root, PLUGIN_CONFIG.CONFIG)
                suite_name = read_toml(config)["suite_name"]
                break

        # get the suite directory
        for dirpath, dirnames, filename in os.walk(download_path):
            if suite_name in dirnames:
                suite_path = os.path.join(dirpath, suite_name)
                logger.info(f"the directory path is {suite_path}")
                break

        # Move to the suites dir.
        suites = self.dir_loader.load(suite_path)
        delete(download_path)
        return suites


class S3BucketLoader(UrlLoader):
    """load plugin from an url source"""

    def __init__(self, download_dir, suites_dir) -> None:
        """initialize the plugin loader

        Args:
            download_dir (str): path to where the plugin suite will be downloaded
            suites_dir (str): path to where the plugin will be stored after
                              download
        """
        self.download_dir = download_dir
        self.suites_dir = suites_dir
        try:
            self.fernet = Fernet(PLUGIN_CONFIG.EN_KEY)
            self.aws_api_key = self.fernet.decrypt(
                PLUGIN_CONFIG.ENCRYPTED_API_KEY
            ).decode()
            self.aws_id = self.fernet.decrypt(PLUGIN_CONFIG.ENCRYPTED_API_ID).decode()
        except Exception as e:
            logger.error(e, exc_info=e)
            self.fernet = None
            self.aws_api_key = None
            self.aws_id = None

    def is_supported_url(self, bucket: str) -> bool:
        """given a url, returns true if the url is supported by the
             github loader

        Args:
            url (str): the url string
        """
        r3 = boto3.resource(
            "s3", aws_access_key_id=self.aws_id, aws_secret_access_key=self.aws_api_key
        )
        try:
            r3.meta.client.head_bucket(Bucket=bucket)
            return True
        except ParamValidationError:
            return False
        except Exception as e:
            logger.error(e, exc_info=e)
            return False

    def load(self, bucket: str) -> List[PluginSuite]:
        """download the plugin from a given url and stored a copy of the
            plugins in the suites directory

        Args:
            url (str): url for downloading the suite
            suites_directory  (str): path to where a copy of the plugin suite
                                    will be store

        Returns:
            PluginSuite: return a PluginSuite object that stores the loaded suite
        """
        if not self.is_supported_url(bucket):
            return False

        s3 = boto3.client(
            "s3", aws_access_key_id=self.aws_id, aws_secret_access_key=self.aws_api_key
        )

        pluginsuites = []
        # get all object from teh bucket
        objects = s3.list_objects_v2(Bucket=bucket)["Contents"]
        for obj in objects:
            key = obj["Key"]
            if "zip" in key:
                # Generate a presigned URL for the object
                url = s3.generate_presigned_url(
                    "get_object", Params={"Bucket": bucket, "Key": key}, ExpiresIn=3600
                )
                url = url[0 : url.index("?")]
                logger.info(f"loading plugin from url {url}")
                ZipLoader = S3ZipLoader(self.download_dir, self.suites_dir)
                pluginsuites.extend(ZipLoader.load(url))
        return pluginsuites
