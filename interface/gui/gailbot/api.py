# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-10 14:06:17
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-18 23:00:46

import sys
import os
from typing import List, Dict, Any, Union, Tuple
from gailbot.core.engines import Engine
from gailbot.services.controller import ServiceController
from gailbot.workspace import WorkspaceManager
from .plugins import PluginSuite
from gailbot.core.utils.logger import makelogger
logger = makelogger("gb_api")
class GailBot:
    """
    Class for API wrapper
    """
    def __init__(
        self,
        user_root : str 
    ):
        self.ws_manager: WorkspaceManager = WorkspaceManager(user_root)
        self.gb: ServiceController = ServiceController(
            self.ws_manager, load_exist_setting = True)
        self.reset_workspace()
        logger.info("initialize the gailbot api")
        
    
    def reset_workspace(self):
        """
        Resets the workspace: clears the old workspace and initializes a new one.

        Args:
            self

        Returns:
            No return but instantiates a new workspace.
        """
        self.ws_manager.clear_gb_temp_dir()
        self.ws_manager.init_workspace()
        
        ### Organizer Service

    def transcribe(self, sources: List[str] = None):
        return self.gb.transcribe(sources)
   
    def add_sources(
        self, 
        src_output_pairs : List [Tuple [str, str]]
    ) -> bool:
        """
        Adds a given list of sources

        Args:
            self
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
            self
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
            self
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
            self
            name: str: Name of the source to look for

        Returns:
            Bool: True if the given name corresponds to an existing source, false if not
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
            self
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
            self
            setting_name: str: Name of the setting to save
        
        Returns:
            Bool: True if setting was successfully saved, false if not
        """
        return self.gb.save_setting(setting_name)

    def get_setting_dict(self, setting_name) -> Union[bool, Dict[str, Union[str, Dict]]]:
        return self. gb.get_setting_dict(setting_name)
    
    
    def get_source_setting_dict(self, source_name) -> Union[bool, Dict[str, Union[str, Dict]]]:
        return self.gb.get_source_setting_dict(source_name)
    
    def get_serialized_setting_data(self) -> Dict[str, Dict]:
        return self.gb.get_serialized_setting_data()
     
    def rename_setting(
        self, 
        old_name: str,
        new_name: str
    ) -> bool:
        """
        Renames a given setting to a given new name

        Args:
            self
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
            self
            setting_name: str: name of the setting to update
            new_setting: Dict[str, str]: dictionary representation of 
                the new structure of the setting

        Returns:
            Bool: true if setting was successfully updated, false if not
        """
        return self.gb.update_setting(setting_name, new_setting)
        
    def get_engine_setting(
        self, 
        setting_name: str, 
    ) -> Dict[str, str]:
        """
        Accesses the engine setting of a given setting

        Args:
            self
            setting_name: str: name of the setting to get the engine setting of

        Returns:
            Dict[str, str]: dictionary representation of the engine setting
        """
        return self.gb.get_engine_setting(setting_name)
    
    def get_plugin_setting(
        self, 
        setting_name: str
    ) -> Dict[str, str]:
        """
        Accesses the plugin setting of a given setting

        Args:
            self
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
            self
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
            self
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
            self
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
            self
            sources: List[str]: list of names of the sources to which to apply the given setting
            setting: str: name of the setting to apply to the given sources
            overwrite: bool: determines if it should overwrite from an existing setting
                Defaults to true

        Returns: 
            Bool: true if setting was successfully applied, false if not

        """
        return self.gb.apply_setting_to_sources(sources, setting, overwrite)
   
    def register_plugin_suite(
        self, 
        plugin_source : str
    ) -> str:
        """
        Registers a gailbot plugin suite

        Args:
            self
            plugin_source : str: Name of the plugin suite to register

        Returns:
        """
        return self.gb.register_plugin_suite(plugin_source)
    
    def get_plugin(
            self, 
            suite_name
        ) -> PluginSuite:
        """
        Gets the plugin suite with a given name

        Args:
            self
            suite_name: string name of the given plugin suite

        Returns:
            PluginSuite with the given name
        """
        return self.gb.get_plugin(suite_name) 
    
    def is_plugin(self, suite_name:str)-> bool:
        """
        Determines if a given plugin suite is an existing plugin suite

        Args:
            self
            suite_name: str: name of the plugin suite of which to determine existence

        Returns:
            Bool: true if given plugin suite exists, false if not
        """
        return self.gb.is_plugin(suite_name) 
   
    def delete_plugin(self, suite_name:str) -> bool:
        """
        Removes the given plugin suite

        Args:
            self
            suite_name: str: name of the plugin suite to delete

        Returns:
            Bool: true if plugin suite was successfully removed, false if not
        """
        return self.gb.delete_plugin(suite_name)
    
   
    