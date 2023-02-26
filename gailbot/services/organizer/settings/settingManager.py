from typing import Dict, Union, List
from .settingObject import SettingObject
import os
from gailbot.core.utils.general import (
    is_file, 
    is_directory, 
    read_toml, 
    get_name, 
    make_dir, 
    delete,
    filepaths_in_dir)
from gailbot.core.utils.logger import makelogger
from gailbot.configs import path_config_loader
from gailbot.workspace import WorkspaceManager
PATH_CONFIG = path_config_loader()

logger = makelogger("setting_manager")

class ExistingSettingName(Exception):
    def __init__(self, name: str, *args: object) -> None:
        super().__init__(*args)
        self.name = name
    def __str__(self) -> str:
        return f"the setting name {self.name} already exist"

class SettingManager():
    """
    Manages all available settings 
    """
    settings : Dict[str , SettingObject] = dict()
    workspace = WorkspaceManager.setting_src
    
    def __init__(self, load_exist: bool = True) -> None:
        if not is_directory(self.workspace):
            make_dir(self.workspace)
            
        if load_exist: 
            setting_files = filepaths_in_dir(self.workspace, ["toml"])
            for file in setting_files:
                self.load_setting_from_file(file)
    
    def get_setting_names(self) -> List[str]:
        """ return a list of available setting names 

        Returns:
            List[str]: a list of setting names 
        """
        return list(self.settings.keys())
    
    def remove_setting(self, name: str) -> bool:
        """ given the setting name, remove the setting and the local 
            setting file
        Args:
            name (str): the name that identify the setting

        Returns:
            bool: return true if the removal is successful, false if
                  the setting does not exist 
        """
        if self.is_setting(name):
            self.settings.pop(name)
            if is_file(self.get_setting_path(name)):
                delete(self.get_setting_path(name))
            return True
        else:
            return False
    
    def get_setting(self, name:str) -> Union [SettingObject, bool]:
        """ given the setting name, return the corresponding setting 

        Args:
            name (str): a name that identifies the setting

        Returns:
            Union [SettingObject, bool]: return the setting object if the 
            setting is found, return false if the setting does not exist 
        """
        if self.is_setting(name):
            return self.settings[name]
        else:
            return False
        
    def add_new_setting(self, name: str, setting: Dict[str, str], 
                        overwrite: bool = False) -> Union[bool, str]:
        """ add a new setting 

        Args:
            name (str): the setting name that identifies the setting
            setting (Dict[str, str]): a dictionary that stores the setting
            overwrite (bool, optional): if true, the given setting will overwrite
            an existing setting if a setting with the same name exist.
            Defaults to False.

        Returns:
            Union[bool, str]: True if the setting creates successfully, 
                              False otherwise 
        
        Raises:
            ExistingSettingName: raised when the setting name already exist
                                 and the overwrite option is set to false 
        """
        if self.is_setting(name) and (not overwrite): 
            raise ExistingSettingName(name)
        try:
            setting: SettingObject = SettingObject(setting, name)
            assert setting.engine_setting
            self.settings[name] = setting
            return True
        except Exception as e:
            logger.error(e)
            return False

    def is_setting(self, name: str) -> bool:
        """ tell if a setting exists in the setting manager

        Args:
            name (str): the setting name

        Returns:
            bool: return true if the given name is an existing setting, false
                  otherwise 
        """
        return name in self.get_setting_names()

    def update_setting(self, name: str, src: Dict[str, str]) -> bool:
        """ update the setting

        Args:
            name (str): setting name
            src (Dict[str, str]): the updated setting content

        Returns:
            bool:   return true if the setting is updated, false if the 
                    setting does not exist or the new setting dictionary 
                    cannot be validated 
        """
        if self.is_setting(name):
            try:
                assert self.settings[name].update_setting(src)
                assert self.save_setting(name)
                return True
            except Exception as e:
                logger.error(e)
        else:
            return False

    def rename_setting(self, name: str, new_name:str) ->bool:
        """ rename a setting 

        Args:
            name (str): the original name of the setting 
            new_name (str): the new name of the setting 

        Returns:
            bool: return true if the setting can be renamed, false 
                  if the setting does not exist or if the new_name
                  has been taken by other existing setting
        """        
        if self.is_setting(name):
            if self.is_setting(new_name):
                logger.error(f"new name{ new_name} has been taken")
                return False
            temp = self.settings.pop(name)
            temp.name = new_name
            self.settings[new_name] = temp
            self.save_setting(new_name)
            if is_file(self.get_setting_path(name)): 
                delete(self.get_setting_path(name))
            logger.info("update_setting")
            return self.settings[new_name] != None
        else:
            logger.error("the setting is not found")
            return False
    
    def save_setting(self, name:str) -> Union[bool, str]:
        """ save the setting as a local file

        Args:
            name (str): the setting name

        Returns:
            Union[bool, str]: return the saved file path if the setting
                              is saved successfully, return false otherwise 
            
        """ 
        try: 
            out_path = self.get_setting_path(name)
            if is_file(out_path):
                delete(out_path)
            self.settings[name].save_setting(out_path) 
            return out_path
        except Exception as e:
            logger.error(e)
            return False   
        
    def load_setting_from_file(self, file_path, overwrite: bool = False) ->bool:
        """ load the setting from local file

        Args:
            file_path (str): the file path
            overwrite (bool, optional): if true, the loaded
            file will overwrite existing setting with same name. Defaults to False.

        Returns:
            bool: return true if the loading is successful, false if the file
            cannot be loaded 
        """
        if is_file(file_path):
            data = read_toml(file_path)
            try:
                name = get_name(file_path)
                data = read_toml(file_path)
                return self.add_new_setting(name, data, overwrite)
            except Exception as e:
                logger.error(e)
                return False
    
    def get_setting_path(self, name:str) -> str:
        """given a setting name, return its path

        Args:
            name (str): the setting name

        Returns:
            str: a path to store the setting file
            
        Note:
            This is a function to form a path to the local setting file 
            in a unified format, the path does not guaranteed to indicate 
            an existing setting file
        """
        return os.path.join(self.workspace, name + ".toml")
    
    def delete_all_settings(self) -> bool:
        """ delete all settings 

        Returns:
            bool: True if the deletion is successful, false if not 
        """
        try:
            for setting in self.get_setting_names():
                if setting != "default":
                    self.remove_setting(setting)
            return True
        except Exception as e:
            logger.error(e)
            return False 