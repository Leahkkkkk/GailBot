from typing import Dict, List, Any, Tuple, Union, Callable

from .organizer import Organizer, SettingDict
from .converter import Converter 
from .pipeline import PipelineService
from ..plugins import PluginManager, PluginSuite
from gailbot.core.utils.logger import makelogger
from gailbot.core.utils.general import get_name
from gailbot.workspace.manager import WorkspaceManager
from gailbot.configs import service_config_loader

CONFIG = service_config_loader()
logger = makelogger("service_controller")
""" Knows about all three sub modules """
class ServiceController:
    def __init__(self, ws_manager: WorkspaceManager, load_exist_setting: bool = False) -> None:
        self.organizer = Organizer(ws_manager.setting_src, load_exist_setting)
        self.converter = Converter(ws_manager)
        self.plugin_manager = PluginManager(ws_manager.plugin_src)
        self.pipeline_service = PipelineService(
            self.plugin_manager, num_threads = CONFIG.thread.transcriber_num_threads) 
    
    def add_sources(self, src_output_pairs: List [Tuple [str, str]]):
        """add a list of sources

        Args:
            src_output_pairs (List[Tuple [str, str]]): a list of pairs that 
            stores the input path and the output path
            
        Returns:
            bool : return true of the sources are added correctly 
        """
        logger.info(src_output_pairs)
        try:
            for src_pair in src_output_pairs:
                (source_path, out_path) = src_pair
                logger.debug(source_path)
                logger.debug(out_path)
                assert self.add_source(source_path, out_path)
            return True
        except Exception as e:
            logger.error(e, exc_info=e)
            return False
        
    def add_source(self, src_path: str, out_path: str) -> bool:
        """add a single source

        Args:
            src_path (str): path to the input source
            out_path (str): path to where the output will be stored

        Returns:
            bool: true if the source can be added 
        """
        logger.info(f"add source {src_path}")
        return self.organizer.add_source(src_path, out_path)
        
    def remove_source(self, name: str) -> bool:
        """remove the source 

        Args:
            name (str): the name of the source, which can be either the 
                        full path to the source or the filename 
            

        Returns:
            bool: return true if the source can be deleted correctly
        """
        return self.organizer.remove_source(name)
    
    def is_source(self, name:str) -> bool:
        """ check if a source exists

        Args:
            name (str): either the name of the source or the path to the source

        Returns:
            bool: return true if the source exists
        """
        return self.organizer.is_source(name)
    
    def create_new_setting(self, name: str, setting: SettingDict) -> bool:
        """ create a new setting

        Args:
            name (str): the name of the setting
            setting (Dict[str, str]): the setting content

        Returns:
            bool: return true if the setting can be created, if the setting uses 
                  an existing name, the setting cannot be created
        """ 
        return self.organizer.create_new_setting(name, setting)
        
    def save_setting(self, setting_name: str) -> bool:
        """ save the setting locally on the disk

        Args:
            setting_name (str): the setting name of the setting

        Returns:
            bool: return true if the setting is saved correctly 
        """
        return self.organizer.save_setting_profile(setting_name)
    
    def rename_setting(self, old_name: str, new_name: str) -> bool:
        """rename a setting

        Args:
            old_name (str): the old name that identifies the setting
            new_name (str): the new name of the setting

        Returns:
            bool: return true if the setting can be renamed correctly, 
                  return false if the new setting name has been taken
        """
        return self.organizer.rename_setting(old_name, new_name)
    
    def update_setting(self, setting_name: str, new_setting: SettingDict) -> bool:
        """updating the setting with new setting content

        Args:
            setting_name (str): the setting name that identifies the setting 
            new_setting (SettingDict): the content of the new settings

        Returns:
            bool: return true if the setting can be updated correctly
        """
        return self.organizer.update_setting(setting_name, new_setting)
   
    def get_all_settings_data(self) -> Dict[str, SettingDict]:
        """ return all settings data in a dictionary 

        Returns:
            Dict[str, SettingDict]: a dictionary that maps the setting name to 
                a setting content
        """
        return self.organizer.get_all_settings_data()
    
    def get_all_settings_name(self) -> List[str]: 
        """ get the names fo available settings

        Returns:
            List[str]: a list of available setting names
        """
        return self.organizer.get_all_settings_name()
    
    def get_src_setting_name(self, source_name: str) -> Union[bool, str]:
        """ given a source, return its setting name

        Args:
            source_name (str): the name of the source

        Returns:
            Union[bool, str]: if the source is found, return its setting name, 
                              else, return false 
            
        """
        if not self.organizer.is_source(source_name):
            return False
        return self.organizer.get_source_setting(source_name).name
     
    def get_plugin_setting(self, setting_name: str) -> Union[bool, List[str]]:
        """ returns the plugin setting of the setting

        Args:
            setting_name (str): name that identifies a setting

        Returns:
            Union[bool, Dict[str, str]]: if the setting is found, return the 
            list of string that identifies which plugins are used, else return 
            false
        """
        return self.organizer.get_plugin_setting(setting_name)
    
    def get_setting_dict(self, setting_name:str) -> Union[bool, SettingDict]:
        """ given a setting name, return the setting content in a dictionary 

        Args:
            setting_name (str): name that identifies a setting

        Returns:
            Union[bool, SettingDict]: if the setting is found, returns its setting 
            content stored in a dictionary, else returns false  
        """
        return self.organizer.get_setting_dict(setting_name)
    
    def get_source_setting_dict(
        self, source_name:str) -> Union[bool, Dict[str, Union[str, Dict]]]:  
        """ given a source name, return the setting content of the source 
            in a dictionary 

        Args:
            source_name (str): name that identifies a source

        Returns:
            Union[bool, SettingDict]: if the source is found, returns its setting 
            content stored in a dictionary, else returns false  
        """
        return self.organizer.get_source_setting(source_name).data
     
    def remove_setting(self, setting_name: str) -> bool:
        """remove a setting 

        Args:
            setting_name (str): the name of the setting that will be removed

        Returns:
            bool: true if the setting is removed, false otherwise 
        """
        return self.organizer.remove_setting(setting_name)
    
    def is_setting(self, name:str ) -> bool:
        """check if a setting exists or not

        Args:
            name (str): names that identifies the settings

        Returns:
            bool: return true if the setting exists, false otherwise
        """
        return self.organizer.is_setting(name)
        
    def get_default_setting_name(self) -> str:
        """
        Accesses an object's default setting name

        Returns:
            string containing the default name
        """
        return self.organizer.get_default_setting_name()
    
    def set_default_setting(self, setting_name:str) -> bool:
        """
        Updates an object's default setting to the given setting name

        Args:
            setting_name:str: new setting name
        
        Returns:
            bool: True if successfully set, false if not
        """
        return self.organizer.set_default_setting(setting_name) 
   
   
    def apply_setting_to_sources(
        self, sources: List[str], setting: str, overwrite: bool = True) -> bool:
        """apply setting to a list of sources

        Args:
            sources (List[str]): a list of string that identifies the sources
            setting (str): the setting name
            overwrite (bool, optional): if true, overwrites  the existing setting 
            . Defaults to True.

        Returns:
            bool: return true if settings can be applied
        """
        return self.organizer.apply_setting_to_sources(sources, setting, overwrite)
    
    def apply_setting_to_source(
        self, source: str, setting: str, overwrite: bool = True) -> bool:
        """apply setting to a source 

        Args:
            sources (str): a string that identifies the source
            setting (str): the setting name
            overwrite (bool, optional): if true, overwrites  the existing setting 
            . Defaults to True.

        Returns:
            bool: return true if settings can be applied
        """
        return self.organizer.apply_setting_to_source(source, setting, overwrite)

    def is_setting_in_use(self, setting_name: str) -> bool:
        """check if a setting is being used by any source

        Args:
            setting_name (str): the name of the setting

        Returns:
            bool: return true if the setting is being used, false otherwise
        """
        return self.organizer.is_setting_in_use(setting_name)    
    
    def add_progress_display(self, source: str, progress_display: Callable):
        """ add a displayer function to the source to track the progress of the 
            source in the pipeline 

        Args:
            source_name (str): the name of the source
            displayer (Callable): a callable function that only takes in 
                                  one argument that stores the progress message 
                                  as a string

        Returns:
            bool: true if the displayer is added correctly, false other wise
        """
        return self.organizer.add_progress_display(source, progress_display)


    def transcribe(self, sources: List[str] = None) -> Tuple [List[str], List[str]]:
        """ return a list of file that was not able to be transcribed, 
            and the transcription result of the rest of the file

        Args:
            sources (List[str], optional): a list of file names. Defaults to None.

        Returns:
           Tuple [List[str], List[str]]: return a tuple of two list, 
                                         the first list stores a list of invalid files, 
                                         the second list stores a list of files that 
                                         fail to be transcribed 
        """
        invalid, fails = [], []
        
        # get configured sources 
        try:
            if not sources:
                source_objs = self.organizer.get_configured_sources(sources)
            else: 
                source_objs = [self.organizer.get_source(name) for name in sources]
            # load to converter 
            payloads, invalid = self.converter(source_objs)
            
            if len(source_objs) != 0:
                logger.info(payloads)
                # put the payload to the pipeline
                fails = self.pipeline_service(payloads=payloads)
                logger.info(f"the failed transcriptions are {fails}")
                logger.info(f"the invalid files are {invalid}")
            
            # remove source from organizer
            if sources:
                for source in sources:
                    self.organizer.remove_source(source)
           
            return invalid, fails
        except Exception as e:
            logger.error(e, exc_info=e)
            return invalid, sources
        
    def register_plugin_suite(self, plugin_source: str) -> Union[List[str], str]:
        """
        Registers a plugin suite to the object's plugin manager

        Args:
            plugin_source: str: plugin suite to register
        
        Returns:
            Union[str, bool]: return the plugin name if successfully registered, 
                              return the string that stores the error message if 
                              the plugin is not registered
        """
        return self.plugin_manager.register_suite(plugin_source)
        
    def get_plugin_suite(self, suite_name) -> PluginSuite:
        """
        Accesses the plugin suite object associated with a given name

        Args:
            suite_name: name of the suite to search for

        Returns:
            PluginSuite: found plugin suite object
        """
        return self.plugin_manager.get_suite(suite_name)
  
    
    def get_all_plugin_suites(self) -> List[str]:
        """ get names of available plugin suites

        Returns:
            List[str]: a list of available plugin suites name
        """
        return self.plugin_manager.get_all_suites_name()
    
    
    def is_plugin_suite(self, suite_name: str) -> bool:
        """
        Determines if a given name is associated with a plugin suite object in the 
            plugin manager
        
        Args:
            suite_name: str: name of the suite to search for

        Returns:
            bool: True if name is associated with an existing plugin suite in the 
                manager, false if not
        """
        return self.plugin_manager.is_suite(suite_name)
    
    def delete_plugin_suite(self, suite_name: str) -> bool:
        """
        Deletes the plugin suite with the given name from the object's plugin manager

        Args:
            suite_name: str: name of the plugin suite to delete

        Returns:
            bool: True if successfully deleted, false if not
        """
        return self.plugin_manager.delete_suite(suite_name)
    
    def get_plugin_suite_metadata(self, suite_name: str):
        """ get the metadata of a plugin suite identified by suite name

        Args:
            suite_name (str): the name of the suite

        Returns:
            MetaData: a MetaData object that stores the suite's metadata, 
                      
        """
        return self.plugin_manager.get_suite_metadata(suite_name)

    def get_plugin_suite_dependency_graph(self, suite_name: str) :
        """ get the dependency map of the plugin suite identified by suite_name

        Args:
            suite_name (str): the name of the suite

        Returns:
            Dict[str, List[str]]: the dependency graph of the suite
        """
        return self.plugin_manager.get_suite_dependency_graph(suite_name)

    def get_plugin_suite_documentation_path(self, suite_name: str) :
        """ get the path to the documentation map of the plugin suite identified by suite_name

        Args:
            suite_name (str): the name of the suite

        Returns:
            str: the path to the documentation file
        """
        return self.plugin_manager.get_suite_documentation_path(suite_name)
    
    
    def is_suite_in_use(self, suite_name:str) -> bool:
        """given a suite_name, check if this suite is used 
           in any of the setting

        Args:
            suite_name (str): the name of the plugin suite

        Returns:
            bool: return true if the suite is used in any of the setting, 
                  false otherwise
        """
        return self.organizer.is_suite_in_use(suite_name)
    
    def is_official_suite(self, suite_name:str) -> bool:
        """given a suite_name, check if the suite identified by the suite_name
           is official

        Args:
            suite_name (str): the name of the suite

        Returns:
            bool: true if the suite is official false otherwise
        """
        return self.plugin_manager.is_official_suite(suite_name)