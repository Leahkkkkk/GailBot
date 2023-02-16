import os 
from typing import Dict, List, Union, TypedDict, Tuple
from pydantic import BaseModel, ValidationError
from gailbot.core.utils.logger import makelogger
from .suite import PluginSuite
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
from urllib.parse import urlparse
from abc import ABC

logger = makelogger("plugin_loader")

class PluginDict(BaseModel):
    """ dictionary type for individual plugin """
    plugin_name: str
    dependencies: List[str]
    module_name: str 
    rel_path: str
    
class ConfDict(TypedDict):
    """ dictionary type for plugin suite configuration dictionary"""
    suite_name: str 
    plugins: List[PluginDict]

class ConfModel(BaseModel):
    """ dictionary type for plugin suite configuration dictionary"""
    suite_name: str 
    plugins: List[PluginDict]

class PluginLoader(ABC):
    """ base class for plugin loader """
    def load(self, *args, **kwargs) -> PluginSuite:
        raise NotImplementedError()

class UrlLoader(ABC):
    """ base class for loading plugin from url """
    def __init__(self, download_dir, suites_dir) -> None:
        self.download_dir = download_dir 
        self.suites_dir = suites_dir
        self.dir_loader = PluginDirectoryLoader(suites_dir)
        super().__init__()
    
    def is_valid_url(self, url: str) -> bool:
        """ 
        check if the url string is valid 

        Args:
            url (str): a string that represent the url 

        Returns:
            bool: true if the string is valid url false otherwise
        """
        if not type(url) == str: 
            return False
        result = urlparse(url)
        if not all([result.scheme, result.netloc]):
            return False
        return True
    
    def is_supported_url(self, url: str) -> bool:
        """
        check if the url is supported
        """
        raise NotImplementedError
    
    def load(self, url: str) -> PluginSuite:
        """ load the source from the url """
        raise NotImplementedError
    
class PluginURLLoader(PluginLoader):
    """ 
    plugin loader to download and load plugin suite from url,
    the loader can currently recognize and download plugin suite from 
    github
    """
    def __init__(
        self,
        download_dir: str,
        suites_dir: str) -> None:
        super().__init__()
        self.download_dir = download_dir 
        
        self.url_loaders: List[UrlLoader] = [
            GitHubURLLoader(download_dir, suites_dir)]

    @property
    def supported_url_source(self):
        """ return a list of supported url downloading source """
        return ["github"] 
    
    def load(self, url : str) -> Union [PluginSuite, bool]:
        """ 
        load the plugin suite from the url if the url is supported by the 
        list of the loader available, 

        Args:
            url (str): url string 

        Returns:
            PluginSuite: loaded plugin suite object if the url is supported 
            Bool: return false if the url is not supported by current url loader
        """
        for loader in self.url_loaders:
            if not loader.is_valid_url(url):
                return False
            if loader.is_supported_url(url): 
                return loader.load(url)
            
class GitHubURLLoader(UrlLoader):
    """ load plugin from an url source  """
    def __init__(self, download_dir, suites_dir) -> None:
        """ initialize the plugin loader
        
        Args:
            download_dir (str): path to where the plugin suite will be downloaded 
            suites_dir (str): path to where the plugin will be stored after 
                              download
        """
        super().__init__(download_dir, suites_dir)
     
    def is_supported_url(self, url: str) -> bool:
        """  given a url, returns true if the url is supported by the 
             github loader
        
        Args:
            url (str): the url string
        """
        parsed = urlparse(url)
        if parsed.scheme == 'https' and parsed.netloc == 'github.com':
            return True
        else:
            return False
        
    def load(self, url : str) -> PluginSuite:
        """ download the plugin from a given url and stored a copy of the 
            plugins in the suites directory 

        Args:
            url (str): url for downloading the suite 
            suites_directory  (str): path to where a copy of the plugin suite 
                                    will be store 

        Returns:
            PluginSuite: return a PluginSuite object that stores the loaded suite
        """
        # check if the type is valid
        if not self.is_valid_url(url) or not self.is_supported_url(url):
            return False
        
        download_path = download_from_urls(
            urls = [url],
            download_dir = self.download_dir,
            unzip = True
        )[0]
        
        # get the suite name from the toml file
        for dirpath, dirnames, filenames in os.walk(download_path):
            for file in filenames:
                if get_extension(file) == "toml":
                    suite_name = read_toml(os.path.join(dirpath, file))["suite_name"]
                    break
        
        # get the suite directory 
        for dirpath, dirnames, filename in os.walk(download_path):
            if suite_name in dirnames:
                suite_path = os.path.join(dirpath, suite_name)
                logger.info(f"the directory path is {suite_path}")
                break
            
        # Move to the suites dir.
        return self.dir_loader.load(suite_path)
    
class PluginDirectoryLoader(PluginLoader):
    """ load the plugin suite from a directory that contains all source 
        script implementing the plugins, and a toml file that stores 
        configuration information to load the plugin     
    """
    def __init__(
        self,
        suites_dir : str, 
    ):
        """ initialize a plugin directory loader

        Args:
            suites_dir (str): the path to the directory that stores all the 
                              copies of plugins will be stored and managed 
                              by plugin manager 
        """
        self.suites_dir = suites_dir
        self.toml_loader = PluginTOMLLoader()

    def load(self,
             suite_dir_path: str) -> Union [PluginSuite, bool]:
        """ load the plugin from a directory 

        Args:
            suite_dir_path (str): path to the source directory that contains 
                                  the entire plugin suite                
        Returns:
            return a PluginSuite object that stores the loaded suite
            if the plugin can be successfully loaded, return false otherwise      
        """
        if (not type(suite_dir_path) == str) \
           or (not is_directory(suite_dir_path)):
            logger.info(suite_dir_path)
            logger.error("not a plugin")
            # check for invalid input 
            return False
        
        suite_dir_name = get_name(suite_dir_path)
        logger.info(f"suite name is {suite_dir_name}, suite path is {suite_dir_path}") 
        tgt_path = f"{self.suites_dir}/{get_name(suite_dir_path)}"
       
        if not is_directory(tgt_path):
            copy(suite_dir_path, tgt_path)
        
        conf = filepaths_in_dir(suite_dir_path,["toml"])[0]
        return self.toml_loader.load(conf, suite_dir_name, self.suites_dir)

class PluginTOMLLoader(PluginLoader):
    """  import all modules in the plugin, all plugin sources and dependencies 
         are described in a configuration file in toml format 
    """
    def __init__(self):
        self.dict_config_loader = PluginDictLoader()

    def load(self, conf_path: str, suite_name: str,  suites_directory : str) -> PluginSuite:
        """  given the path to configuration file of one plugin suite, and 
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
            conf.update({
                "path" : get_parent_path(conf_path)
            })
            return self.dict_config_loader.load(conf, suites_directory)
        else:
            logger.error(f"Error: {conf}")
            return False


    @staticmethod
    def validate_config(
        conf_path: str, suite_name: str) -> Tuple [bool, Union[str, Dict]]:
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
        if not type(conf_path) == str :
            return (False, "Invalid file path")
        if (not os.path.isfile(conf_path)) or \
                (not get_extension(conf_path) == "toml"):
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
    """ load a plugin suite from a dictionary that contains the configuration 
        of all plugin dependencies and sources 
    """
    def load(self, dict_conf : Dict, suites_directory : str) -> PluginSuite:
        if not type(dict_conf) == dict:
            return
        suite = PluginSuite(dict_conf, suites_directory)
        if suite.is_ready:
            return suite
        else:
            return False

