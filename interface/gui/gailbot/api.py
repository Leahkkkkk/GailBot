# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-10 14:06:17
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-18 23:00:46

from typing import List, Dict, Union, Tuple, Callable

from gailbot.services import ServiceController, SettingDict 
from gailbot.workspace import WorkspaceManager
from .plugins.suite import PluginSuite
from gailbot.core.utils.logger import makelogger

logger = makelogger("gb_api")
class GailBot:
    """
    Class for API wrapper
    """
    def __init__(
        self,
        ws_root : str 
    ):
        """ initialize an gailbot object that provides a suite of functions
            to interact with gailbot

        Args:
            ws_root (str): the path to workspace root
        """
        self.ws_manager: WorkspaceManager = WorkspaceManager(ws_root)
        self.init_workspace()
        logger.info("workspace manager initialized")
        self.gb: ServiceController = ServiceController(
            self.ws_manager, load_exist_setting = True)
        logger.info("gailbot service controller initialized")
        
    def init_workspace(self):
        """
        Resets the workspace: clears the old workspace and initializes a new one.

        Returns:
            No return but instantiates a new workspace.
        """
        try:
            self.ws_manager.clear_gb_temp_dir()
            self.ws_manager.init_workspace()
            return True
        except Exception as e:
            logger.error(f"failed to reset workspace due to the error {e}", exc_info=e)
            return False
    
    
    def transcribe(self, sources: List[str] = None) -> Tuple[List[str], List[str]]:
        """ given a list of the source name, and transcribe the sources 

        Args:
            sources (List[str], optional): a list of source name, which 
            can be either a list of source paths or the file name of the 
            source file without the file extension
            if sources is None, the default is to transcribe all sources 
            that have been configured

        Returns:
            Tuple[bool, List[str]]: 
                returns a tuple of two lists of string 
                the first lists consist of files that are not valid input 
                the second lists consist of files that fails to be processed 
            
        """
        return self.gb.transcribe(sources)
   
    def add_sources(
        self, 
        src_output_pairs : List [Tuple [str, str]]
    ) -> bool:
        """
        Adds a given list of sources

        Args:
            src_output_pairs: List [Tuple [str, str]]: List of Tuples of strings 
                to strings, each representing the source path and output path of 
                a source to add
        
        Returns: 
            Bool: True if each given source was successfully added, false if not
        """
        return self.gb.add_sources(src_output_pairs)
    
    def add_source(
        self,
        source_path : str,
        output_dir : str
    ) -> bool:
        """
        Adds a given source

        Args:
            source_path : str: Source path of the given source
            output_dir : str: Path to the output directory of the given source
        
        Returns: 
            Bool: True if the given source was successfully added, false if not
        """
        return self.gb.add_source(source_path,output_dir)

    def remove_source(
            self, 
            source_name : str
        ) -> bool:
        """
        Removes the given source

        Args:
            source_name : str: Name of the existing source to remove
        
        Returns: 
            Bool: True if source was successfully removed, false if not
        """
        return self.gb.remove_source(source_name)

    def is_source(
            self, 
            name : str
        ) -> bool:
        """
        Determines if a given name corresponds to an existing source

        Args:
            name: str: Name of the source to look for

        Returns:
            Bool: True if the given name corresponds to an existing source, 
                  false if not
        """
        return self.gb.is_source(name)
    
    def create_new_setting(
            self, 
            name : str, 
            setting : Dict[str, str]
        ) -> bool:
        """
        Creates a new setting profile

        Args:
            name: str: Name to assign to the newly created setting
            setting : Dict[str, str]: Dictionary representation of the setting

        Returns:
            None
        """
        return self.gb.create_new_setting(name, setting)
    
    def get_src_setting_name(self, source_name:str) -> Union[bool, str]:
        """given a source name, return the setting name applied to the source

        Args:
            source_name (str): the name that identify the source

        Returns:
            Union[bool, str]: if the source is found, return the setting name 
                              applied to the source, else return false
        """
        return self.gb.get_src_setting_name(source_name)    

    def save_setting(
        self,
        setting_name: str
    ) -> bool:
        """
        Saves the given setting

        Args:
            setting_name: str: Name of the setting to save
        
        Returns:
            Bool: True if setting was successfully saved, false if not
        """
        return self.gb.save_setting(setting_name)
     
    def get_source_setting_dict(self, source_name) -> Union[bool, SettingDict]:
        """ 
        Given a source, returns its setting content as a dictionary

        Args:
            source_name (str): the name of the source

        Returns:
            Union[bool, Dict[str, Union[str, Dict]]]:  a dictionary that stores
            the source setting content
        """
        return self.gb.get_source_setting_dict(source_name)
    
    def get_setting_dict(self, setting_name:str) -> Union[bool, SettingDict]:
        """ 
        Given a setting name, returns the setting content in a dictionary 

        Args:
            setting_name (str): name that identifies a setting

        Returns:
            Union[bool, SettingDict]: if the setting is found, returns its setting 
            content stored in a dictionary, else returns false  
        """
        return self.gb.get_setting_dict(setting_name)
    
    def get_all_settings_data(self) -> Dict[str, SettingDict]:
        """
        given a setting name, return the setting content in a dictionary format 

        Args:
            setting_name (string): setting name

        Returns:
            Union[bool, Dict[str, Union[str, Dict]]]: the setting content
        """
        return self.gb.get_all_settings_data()
    
    def get_all_settings_name(self) -> List[str]:
        """ get the names fo available settings

        Returns:
            List[str]: a list of available setting names
        """
        return self.gb.get_all_settings_name()
        
    def rename_setting(
        self, 
        old_name: str,
        new_name: str
    ) -> bool:
        """
        Renames a given setting to a given new name

        Args:
            old_name: str: original name of the setting to rename
            new_name: str: name to rename the setting to

        Returns:
            Bool: True if setting was successfully renamed, false if not

        """
        return self.gb.rename_setting(old_name, new_name)

    def update_setting(
        self, 
        setting_name: str, 
        new_setting: Dict[str, str]
    ) -> bool:
        """
        Updates a given setting to a newly given structure

        Args:
            setting_name: str: name of the setting to update
            new_setting: Dict[str, str]: dictionary representation of 
                the new structure of the setting

        Returns:
            Bool: true if setting was successfully updated, false if not
        """
        return self.gb.update_setting(setting_name, new_setting)
        
    def get_plugin_setting(
        self, 
        setting_name: str
    ) -> Dict[str, str]:
        """
        Accesses the plugin setting of a given setting

        Args:
            setting_name: str: name of the setting to get the plugin setting of

        Returns:
            Dict[str, str]: dictionary representation of the plugin setting
        """
        return self.gb.get_plugin_setting(setting_name)
    
    def remove_setting(
        self,
        setting_name: str
    ) -> bool:
        """
        Removes the given setting

        Args:
            setting_name: str: name of the setting to remove

        Returns:
            Bool: True if setting was successfully removed, false if not
        """
        return self.gb.remove_setting(setting_name)
    
    def is_setting(
        self,
        name: str
    ) -> bool:
        """
        Determines if a given setting name corresponds to an existing setting

        Args:
            name: str: name of the setting to search fort

        Returns:
            Bool: True if given setting is an existing setting, false if not
        """
        return self.gb.is_setting(name)
    
    def apply_setting_to_source(
        self, 
        source: str, 
        setting: str, 
        overwrite: bool = True
    ) -> bool:
        """
        Applies a given setting to a given source

        Args:
            source: str: name of the source to which to apply the given setting
            setting: str: name of the setting to apply to the given source
            overwrite: bool: determines if it should overwrite from an existing setting
                Defaults to true

        Returns: 
            Bool: true if setting was successfully applied, false if not
        """
        return self.gb.apply_setting_to_source(source, setting, overwrite)
    
    def apply_setting_to_sources(
        self, 
        sources: List[str], 
        setting: str, 
        overwrite: bool = True
    ) -> bool:
        """
        Applies a given setting to a given list of sources

        Args:
            sources: List[str]: list of names of the sources to which to apply the given setting
            setting: str: name of the setting to apply to the given sources
            overwrite: bool: determines if it should overwrite from an existing setting
                Defaults to true

        Returns: 
            Bool: true if setting was successfully applied, false if not

        """
        return self.gb.apply_setting_to_sources(sources, setting, overwrite)
   
    def is_setting_in_use(self, setting_name: str) -> bool:
        """check if a setting is being used by any source

        Args:
            setting_name (str): the name of the setting

        Returns:
            bool: return true if the setting is being used, false otherwise
        """
        return self.gb.is_setting_in_use(setting_name)    
    
    def get_default_setting_name(self) -> str:
        """ get the name of current default setting

        Returns:
            str: the name of current default setting
        """
        return self.gb.get_default_setting_name()
   
   
    def set_default_setting(self, setting_name)-> bool:
        """set the default setting to setting name

        Args:
            setting_name (str): the name of the default setting 

        Returns:
            bool: true if default setting is set correctly
        """
        return self.gb.set_default_setting(setting_name)
    
    def register_plugin_suite(
        self, 
        plugin_source : str
    ) -> Union[List[str], str]:
        """
        Registers a gailbot plugin suite

        Args:
            plugin_source : str: Name of the plugin suite to register

        Returns:
            return the a list of plugin name if the plugin is registered, 
            return the string that stores the error message if the pluginsuite 
            is not registered
        """
        return self.gb.register_plugin_suite(plugin_source)
    
    def get_plugin_suite(
            self, 
            suite_name
        ) -> PluginSuite:
        """
        Gets the plugin suite with a given name

        Args:
            suite_name: string name of the given plugin suite

        Returns:
            PluginSuite with the given name
        """
        return self.gb.get_plugin_suite(suite_name) 
    
    def is_plugin_suite(self, suite_name:str)-> bool:
        """
        Determines if a given plugin suite is an existing plugin suite

        Args:
            suite_name: str: name of the plugin suite of which to determine existence

        Returns:
            Bool: true if given plugin suite exists, false if not
        """
        return self.gb.is_plugin_suite(suite_name) 
   
    def delete_plugin_suite(self, suite_name:str) -> bool:
        """
        Removes the given plugin suite

        Args:
            suite_name: str: name of the plugin suite to delete

        Returns:
            Bool: true if plugin suite was successfully removed, false if not
        """
        return self.gb.delete_plugin_suite(suite_name)
   
    def add_progress_display(self, source: str, displayer: Callable) -> bool:
        """
        Add a function displayer to track for the progress of source, 

        Args:
            source (str): the name of the source
            displayer (Callable): displayer is a function that takes in a string as 
                                  argument, and the string encodes the progress of 
                                  the source

        Returns:
            bool: return true if the displayer is added, false otherwise
        """
        return self.gb.add_progress_display(source, displayer)

    def get_all_plugin_suites(self) -> List[str]:
        """ get names of available plugin suites

        Returns:
            List[str]: a list of available plugin suites name
        """
        return self.gb.get_all_plugin_suites()
    
    def get_plugin_suite_metadata(self, suite_name:str) -> Dict[str, str]:
        """ get the metadata of a plugin suite identified by suite name

        Args:
            suite_name (str): the name of the suite

        Returns:
            MetaData: a MetaData object that stores the suite's metadata, 
                      
        """
        return self.gb.get_plugin_suite_metadata(suite_name)

    def get_plugin_suite_dependency_graph(self, suite_name:str) -> Dict[str, List[str]]:
        """ get the dependency map of the plugin suite identified by suite_name

        Args:
            suite_name (str): the name of the suite

        Returns:
            Dict[str, List[str]]: the dependency graph of the suite
        """
        return self.gb.get_plugin_suite_dependency_graph(suite_name)

    def get_plugin_suite_documentation_path(self, suite_name:str) -> str:
        """ get the path to the documentation map of the plugin suite identified by suite_name

        Args:
            suite_name (str): the name of the suite

        Returns:
            str: the path to the documentation file
        """
        return self.gb.get_plugin_suite_documentation_path(suite_name)
    
    def is_suite_in_use(self, suite_name:str) -> bool:
        """given a suite_name, check if this suite is used 
           in any of the setting

        Args:
            suite_name (str): the name of the plugin suite

        Returns:
            bool: return true if the suite is used in any of the setting, 
                  false otherwise
        """
        return self.gb.is_suite_in_use(suite_name)
    
    def is_official_suite(self, suite_name:str) -> bool:
        """given a suite_name, check if the suite identified by the suite_name
           is official

        Args:
            suite_name (str): the name of the suite

        Returns:
            bool: true if the suite is official false otherwise
        """
        return self.gb.is_official_suite(suite_name)

    def reset_workspace(self) -> bool:
        """ reset the gailbot workspace
        """
        return self.ws_manager.reset_workspace()

    def get_suite_source_path(self, suite_name: str) -> str:
       """
       given the name of the  suite , return the path to the source 
       code of the suite
       """ 
       return self.gb.get_suite_path(suite_name)