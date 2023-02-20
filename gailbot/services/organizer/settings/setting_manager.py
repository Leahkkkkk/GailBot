from typing import Dict, Union, List
from .setting_object import SettingObject
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
from ...organizer import PATH_CONFIG

logger = makelogger("setting_manager")

class SettingManager():
    """
    Manages all available settings 
    """
    settings : Dict[str , SettingObject] = dict()
    workspace = PATH_CONFIG.gailbot_data.setting_src # TODO: store this in a toml file 
    
    def __init__(self, load_exist: bool = True) -> None:
        if not is_directory(self.workspace):
            make_dir(self.workspace)
        if load_exist: 
            setting_files = filepaths_in_dir(self.workspace, ["toml"])
            for file in setting_files:
                self.load_setting_from_file(file)
    
    def get_setting_names(self) -> List[str]:
        return list(self.settings.keys())
    
    def remove_setting(self, name: str) -> bool:
        if self.is_setting(name):
            self.settings.pop(name)
            if is_file(self.get_setting_path(name)):
                delete(self.get_setting_path(name))
            return True
        else:
            return False
    
    def get_setting(self, name:str) -> Union [SettingObject, bool]:
        if self.is_setting(name):
            return self.settings[name]
        else:
            return False
        
    def add_new_setting(self, name: str, setting: Dict[str, str], overwrite: bool = False) -> Union[bool, str]:
        if self.is_setting(name) and (not overwrite): 
            return "ERROR: the setting name has been taken"
        try:
            self.settings[name] =  SettingObject(setting, name)
            return True
        except Exception as e:
            logger.error(e)
            return False

    def is_setting(self, name: str) -> bool:
        return name in self.get_setting_names()

    def update_setting(self, name: str, src: Dict[str, str]) -> bool:
        if self.is_setting(name):
            return self.settings[name].update_setting(src)
        else:
            return False

    def rename_setting(self, name: str, new_name:str) ->bool:
        """ TODO: test this function """
        if self.is_setting(name):
            temp = self.settings.pop(name)
            temp.name = new_name
            self.settings[new_name] = temp
            self.save_setting(new_name)
            if is_file(self.get_setting_path(name)):
                delete(self.get_setting_path(name))
            return self.settings[new_name] != None
        else:
            return False
    
    def save_setting(self, name:str) -> Union[bool, str]:
        try: 
            out_path = self.get_setting_path(name)
            self.settings[name].save_setting(out_path) 
            return out_path
        except Exception as e:
            logger.error(e)
            return False   
        
    def load_setting_from_file(self, file_path, overwrite: bool = False) ->bool:
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
        return os.path.join(self.workspace, name + ".toml")