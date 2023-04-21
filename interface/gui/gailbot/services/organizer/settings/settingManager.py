from typing import Dict, Union, List
import os

from .objects import SettingDict, SettingObject, PluginSuiteSetObj, EngineSetObj

from gailbot.core.utils.general import (
    is_file, 
    is_directory, 
    read_toml, 
    get_name, 
    make_dir, 
    delete,
    filepaths_in_dir)
from gailbot.core.utils.logger import makelogger

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
    profiles : Dict[str, SettingObject] = dict()
    engine_settings  : Dict[str, EngineSetObj]   = dict()
    
    def __init__(self, workspace:str, load_exist: bool = True) -> None:
        """ constructing the setting manager

        Args:
            workspace (str): the path to the directory stores all the setting files
            load_exist (bool, optional): if true , load existing setting in workspace. Defaults to True.
        """
        self.workspace = workspace
        self.engine_set_space = os.path.join(workspace, "engine_setting")
        self.default_setting = None
        self.default_engine_setting = None 
        
        if not is_directory(self.workspace):
            make_dir(self.workspace)
        
        if not is_directory(self.engine_set_space):
            make_dir(self.engine_set_space)
            
        if load_exist: 
            engine_files = filepaths_in_dir(self.engine_set_space, ["toml"])
            for file in engine_files:
                self.load_set_from_file(file, self.add_new_engine)
                
            setting_files = filepaths_in_dir(self.workspace, ["toml"])
            for file in setting_files:
                self.load_set_from_file(file, self.add_new_setting)
    
    def load_set_from_file(self, file_path, addfun, overwrite: bool = False) ->bool:
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
                return addfun(name, data, overwrite)
            except Exception as e:
                logger.error(e, exc_info=e)
                return False
    
    #####################################################################
    #               Functions for managing engine setting               #
    #####################################################################
    def get_engine_setting_names(self) -> List[str]:
        """return a list of available engine setting name

        Returns:
            List[str]: a list of engine setting names
        """
        return list(self.engine_settings.keys())

    def add_new_engine(self, name, engine:Dict[str, str], overwrite: bool = False):
        """add a new engine setting

        Args:
            name (str): the name of the engine setting
            engine (Dict[str, str]): the data of the engine setting, 
                                     one required field is the type of the 
                                     engine 
            
            overwrite (bool, optional): if True, overwrite the existing engine s
                                        etting with the same name. Defaults to False.

        Raises:
            ExistingSettingName: if the engine setting name has been taken, and overwrite is set to False

        Returns:
            bool: return true if the setting is successfully added, false otherwise 
        """ 
        if self.is_engine_setting(name) and (not overwrite): 
            raise ExistingSettingName(name)
        try:
            setting: EngineSetObj = EngineSetObj(engine, name)
            assert setting.engine_setting
            self.engine_settings[name] = setting
            self.save_engine_setting(name)
            return True
        except Exception as e:
            logger.error(e, exc_info=e)
            return False
    
    def remove_engine_setting(self, name):
        """remove the engine setting from the disk 

        Args:
            name (str): the name of the engine setting

        Returns:
            bool: return true if the engine setting is removed successfully 
        """
        try:
            assert self.is_engine_setting(name)
            assert not self.engine_settings[name].is_in_use()
            del self.engine_settings[name]
            if is_file(self.get_engine_src_path(name)):
                delete(self.get_engine_src_path(name))
            return True 
        except Exception as e:
            logger.error(e, exc_info=e) 
            return False
        
    def is_engine_setting_in_use(self, name)->bool:
        """check if the engine setting is in use 

        Args:
            name (str): the name of the engine setting
        """
        return self.engine_settings[name].is_in_use()
    
    def is_engine_setting(self, name):
        """check if the given setting is engine setting

        Args:
            name (str): the name that identify the engine setting

        Returns:
            bool: true if the setting is engine setting false otherwise 
        """
        return name in self.engine_settings
    
    def save_engine_setting(self, name:str) -> Union[bool, str]:
        """save the setting as a local file 

        Args:
            name (str): the setting name

        Returns:
            Union[bool, str]: return the saved file path if the setting is 
                              saved successfully, return false otherwise
        """
        try:
            out_path = self.get_engine_src_path(name)
            if is_file(out_path):
                delete(out_path)
            self.engine_settings[name].save_setting(out_path)
            return out_path
        except Exception as e:
            logger.error(e, exc_info=e)
            return False
    
    def update_engine_setting(self, name:str, setting_data: Dict[str, str]) -> bool:
        """
        update the engine setting
        
        Args:
            name(str)
            setting_data(Dict[str, str])
            
        Returns:
            bool
        """ 
        if self.is_engine_setting(name):
            try:
                engine_setting = self.engine_settings[name]
                assert engine_setting.update_setting(setting_data)
                assert self.save_engine_setting(name)
                for profile in engine_setting.applied_in_profiles:
                    ## update the engine setting on the disk 
                    self.save_setting(profile)
                return True
            except Exception as e:
                logger.error(e, exc_info=e)
                return False
                
    def get_engine_src_path(self, name:str) -> str:
        """given a engine setting name, return its path

        Args:
            name (str): the engine setting name

        Returns:
            str: a path to store the setting file
            
        Note:
            This is a function to form a path to the local setting file 
            in a unified format, the path does not guaranteed to indicate 
            an existing setting file
        """
        return os.path.join(self.engine_set_space, name + ".toml")
    
    def rename_engine_setting(self, new_name:str, orig_name:str) -> str:
        raise NotImplementedError()
    
    def get_engine_setting_data(self, name:str) -> Union[bool, Dict[str, str]]:
        if self.is_engine_setting(name):
            return self.engine_settings[name].get_setting_dict()
        else:
            return False
    
    def _get_profile_engine(self, profile_name: str) -> EngineSetObj:
        profile_obj = self.profiles[profile_name]
        engine_obj = self.engine_settings[profile_obj.engine_setting_name]
        return engine_obj

        
    def set_to_default_engine_setting(self, setting_name: str) -> bool:
        """set one setting to be the default setting

        Args:
            name (str): the name of the setting

        Returns:
            bool: return true if the default setting can be set, 
                  false otherwise
        """
        if setting_name in self.profiles:
             self.default_engine_setting = setting_name
             return True
        else:
             return False 

    def get_default_engine_setting_name(self) -> str:
        return self.default_engine_setting
    
    #####################################################################
    #               Functions for managing profile setting              #
    #####################################################################
    def get_setting_names(self) -> List[str]:
        """ return a list of available setting names 

        Returns:
            List[str]: a list of setting names 
        """
        return list(self.profiles.keys())
    
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
            settingObj = self.profiles.pop(name)
            self.engine_settings[settingObj.engine_setting_name].remove_applied_profile(name)
            if is_file(self.get_profile_src_path(name)):
                delete(self.get_profile_src_path(name))
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
            return self.profiles[name]
        else:
            return False
        
    def add_new_setting(self, 
                        name: str, 
                        data: SettingDict,
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
        logger.info(f"get engine {data}")
        if self.is_setting(name): 
            if overwrite:
                self.remove_setting(name)
            else:
                raise ExistingSettingName(name)
        try:
            engine_set_name = data["engine_setting_name"]
            engine_obj = self.engine_settings[engine_set_name]
            plugin_obj = PluginSuiteSetObj(data["plugin_setting"])
            setting: SettingObject = SettingObject(
                engine_setting=engine_obj, 
                engine_setting_name=engine_set_name,
                plugin_setting=plugin_obj,
                name=name)
            self.engine_settings[engine_set_name].add_applied_profile(name)
            assert setting and setting.engine_setting
            self.profiles[name] = setting
            self.save_setting(name)
            return True
        except Exception as e:
            logger.error(e, exc_info=e)
            return False

    def is_setting(self, name: str) -> bool:
        """ tell if a setting exists in the setting manager

        Args:
            name (str): the setting name

        Returns:
            bool: return true if the given name is an existing setting, false
                  otherwise 
        """
        return name in self.profiles

    def update_setting(self, name: str, setting_data: SettingDict) -> bool:
        """ update the setting

        Args:
            name (str): setting name
            setting_data (Dict[str, str]): the updated setting content

        Returns:
            bool:   return true if the setting is updated, false if the 
                    setting does not exist or the new setting dictionary 
                    cannot be validated 
        """
        if self.is_setting(name):
            try:
                profile_setting = self.profiles[name]
                orig_engine = profile_setting.engine_setting.name
                engine_set_name = setting_data["engine_setting_name"]
                engine_obj = self.engine_settings[engine_set_name]
                plugin_obj = PluginSuiteSetObj(setting_data["plugin_setting"])
                assert profile_setting.update_setting(engine_setting=engine_obj, plugin_setting=plugin_obj)
                assert self.save_setting(name)
                return True
            except Exception as e:
                logger.error(e, exc_info=e)
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
            
            temp = self.profiles.pop(name)
            engine_applied = self._get_profile_engine(name)
            engine_applied.remove_applied_profile(name)
            
            temp.name = new_name
            engine_applied.add_applied_profile(new_name)
            self.profiles[new_name] = temp
            self.save_setting(new_name)
            
            if is_file(self.get_profile_src_path(name)): 
                delete(self.get_profile_src_path(name))
            logger.info("update_setting")
            return self.profiles[new_name] != None
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
            out_path = self.get_profile_src_path(name)
            if is_file(out_path):
                delete(out_path)
            self.profiles[name].save_setting(out_path) 
            return out_path
        except Exception as e:
            logger.error(e, exc_info=e)
            return False   
    
    def get_setting_dict(self, setting_name:str) -> Union[bool, SettingDict]:
        """ return the setting data as a dictionary 

        Args:
            setting_name (str): the name that identifies the setting

        Returns:
            Union[bool, SettingDict]: if the setting exists, return the setting 
                                      data, else return false
        """ 
        if setting_name in self.profiles:
            return self.profiles[setting_name].get_data()
        else:
            return False
    
    def get_profile_src_path(self, name:str) -> str:
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
            logger.error(e, exc_info=e)
            return False
        
    def get_all_settings_data(self) -> Dict[str, SettingDict]:
        """ 
        return a dictionary that stores all available setting data 
        """
        setting_dict = dict()
        for key, setting_object in self.profiles.items():
            setting_dict[key] = setting_object.data
            
        logger.info(f"setting data {setting_dict}")
        return setting_dict 

    def set_to_default_setting(self, setting_name: str) -> bool:
        """set one setting to be the default setting

        Args:
            name (str): the name of the setting

        Returns:
            bool: return true if the default setting can be set, 
                  false otherwise
        """
        if setting_name in self.profiles:
             self.default_setting = setting_name
             return True
        else:
             return False 
    


    def get_default_profile_setting_name(self) -> str:
        """get the default setting name

        Returns:
            str: the default setting 
        """
        return self.default_setting
    
    #####################################################################
    #       function for managing plugin setting                        #
    #####################################################################

    def is_suite_in_use(self, suite_name:str) -> bool:
        """given a suite_name, check if this suite is used 
           in any of the setting

        Args:
            suite_name (str): the name of the plugin suite

        Returns:
            bool: return true if the suite is used in any of the setting, 
                  false otherwise
        """
        for setting_obj in self.profiles.values():
            if suite_name in setting_obj.get_plugin_setting():
                return True
        return False
    