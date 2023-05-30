from typing import Dict, List, Union, Callable

from .source import SourceObject, SourceManager
from gailbot.core.utils.logger import makelogger
from .settings import SettingManager, SettingObject, SettingDict
from gailbot.configs import default_setting_loader

logger = makelogger("organizer")
CONFIG = default_setting_loader() 
DEFAULT_SETTING_NAME = CONFIG.profile_name 
DEFAULT_SETTING = CONFIG.profile_data 
DEFAULT_ENGINE_NAME = CONFIG.engine_name
DEFAULT_ENGINE_SETTING = CONFIG.engine_data
class Organizer:
    def __init__(self, setting_workspace: str, load_exist_setting: bool = False) -> None:
        self.setting_manager = SettingManager(setting_workspace, load_exist_setting)
        self.source_manager  = SourceManager()
        
    def add_source(self, source_path: str, output: str) -> Union[str, bool]:
        """
        Adds given source to the output directory

        Args:
            source_path: str: path to the source to add
            output: str: path to the output directory

        Returns: 
            Union[str, bool]: return the name if successfully added, false if not
        """
        try:
            name = self.source_manager.add_source(source_path, output)
            assert name
            return name
        except Exception as e:
            logger.error(e, exc_info=e)
            return False
        
    def remove_source(self, source_name: str) -> bool:
        """
        Removes given source

        Args:
            source_path: str: path to the source to remove

        Returns: 
            bool: True if successfully removed, false if not
        """
        return self.source_manager.remove_source(source_name)
    
    def is_source(self, source_name: str) -> bool:
        """
        Determines if given name corresponds to an existing source

        Args:
            source_name: str: name of potential source

        Returns:
            bool: true if the name corresponds to an existing source, false if not
        """
        return self.source_manager.is_source(source_name)
    
    def get_source(self, source_name: str) -> Union [bool, SourceObject]:
        """
        Accesses source with a given name

        Args:
            source_name: str: source name to access

        Returns:    
            Source object associated with the given name or false if source object is not found
        """
        return self.source_manager.get_source(source_name)
    
    def get_source_outdir(self, source_name: str) -> Union [bool, str]:
        """
        Accesses source output directory with a given name

        Args:
            source_name: str: source name to access

        Returns:    
            a string stores the output of the source
        """

        return self.source_manager.get_source_outdir(source_name)
    
    def get_source_setting(self, source_name: str) -> SettingObject:
        """
        Accesses the settings of a source with a given name

        Args:
            source_name: str: source name whose setting to access

        Returns:    
            Source settings associated with the given name or false if source object is not found
        """
        return self.source_manager.get_source_setting(source_name)
    
    def is_setting_applied(self, source_name: str) -> bool:
        """
        Determines if a given source has configured settings

        Args:
            source_name: str: source name to access

        Returns:
            bool: True if given source is configured, false if not
        """
        return self.source_manager.is_source_configured(source_name)
    
    def apply_setting_to_source(
        self, source_name: str, setting_name:str, overwrite: bool = True) -> bool:
        """apply setting to a source 

        Args:
            sources (str): a string that identifies the source
            setting (str): the setting name
            overwrite (bool, optional): if true, overwrites  the existing setting 
            . Defaults to True.

        Returns:
            bool: return true if settings can be applied
        """
        return self.source_manager.apply_setting_profile_to_source(
            source_name, self.get_setting_obj(setting_name), overwrite)

    def apply_setting_to_sources(
        self, sources: List[str], setting_name:str, overwrite: bool = True)-> bool:
        """apply setting to a list of sources

        Args:
            sources (List[str]): a list of string that identifies the sources
            setting (str): the setting name
            overwrite (bool, optional): if true, overwrites  the existing setting 
            . Defaults to True.

        Returns:
            bool: return true if settings can be applied
        """
        try:
            for source in sources:
                logger.info(f"organizer change {source} setting to {setting_name}")
                assert self.apply_setting_to_source(source, setting_name, overwrite)
            return True
        except Exception as e:
            logger.error(e, exc_info=e)
            return False
    
    def add_progress_display(self, source_name: str, displayer: Callable):
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
        return self.source_manager.add_progress_display(source_name, displayer)
     
    def create_new_setting(
        self, setting_name: str, setting: SettingDict) -> bool: 
        """ create a new setting

        Args:
            name (str): the name of the setting
            setting (Dict[str, str]): the setting content

        Returns:
            bool: return true if the setting can be created, if the setting uses 
                  an existing name, the setting cannot be created
        """ 
        return self.setting_manager.add_new_setting(setting_name, setting)
    
    def save_setting_profile(self, setting_name: str) -> str:
        """ save the setting locally on the disk

        Args:
            setting_name (str): the setting name of the setting

        Returns:
            bool: return true if the setting is saved correctly 
        """
        return self.setting_manager.save_setting(setting_name)
    
   
    def rename_setting(self, setting_name: str, new_name: str) -> bool:
        """rename a setting

        Args:
            old_name (str): the old name that identifies the setting
            new_name (str): the new name of the setting

        Returns:
            bool: return true if the setting can be renamed correctly, 
                  return false if the new setting name has been taken
        """
        try:
            self.setting_manager.rename_setting(setting_name, new_name)
            return True
        except:
            return False
        
   
    def remove_setting(self, setting_name: str) -> bool:
        """remove a setting 

        Args:
            setting_name (str): the name of the setting that will be removed

        Returns:
            bool: true if the setting is removed, false otherwise 
        """
        if not self.setting_manager.is_setting(setting_name):
            return False 
        try:
            assert self.setting_manager.remove_setting(setting_name)
            sources = self.source_manager.get_sources_with_setting(setting_name) 
            for source in sources:
                self.remove_setting_from_source(source)
            return True
        except Exception as e:
            logger.error(e, exc_info=e)
            return False
        
    
    def update_setting(self, setting_name:str, new_setting: Dict[str,str]) -> bool:
        """updating the setting with new setting content

        Args:
            setting_name (str): the setting name that identifies the setting 
            new_setting (SettingDict): the content of the new settings

        Returns:
            bool: return true if the setting can be updated correctly
        """
        return self.setting_manager.update_setting(setting_name, new_setting)
        
    def get_setting_obj(self, setting_name:str) -> SettingObject:
        """ get setting object that is identified by setting name

        Args:
            setting_name (str): the name that identifies the setting object

        Returns:
            SettingObject: a setting object that stores the setting data
        """
        return self.setting_manager.get_setting(setting_name)    
    

    def get_setting_dict(self, setting_name:str) -> Union[bool, SettingDict]:
        """ given a source name, return the setting content of the source 
            in a dictionary 

        Args:
            source_name (str): name that identifies a source

        Returns:
            Union[bool, SettingDict]: if the source is found, returns its setting 
            content stored in a dictionary, else returns false  
        """
        return self.setting_manager.get_setting_dict(setting_name)
    

    def is_setting(self, setting_name: str) -> bool: 
        """check if a setting exists or not

        Args:
            name (str): names that identifies the settings

        Returns:
            bool: return true if the setting exists, false otherwise
        """
        return self.setting_manager.is_setting(setting_name)
    
    
    def is_setting_in_use(self, setting_name: str) -> bool:
        """check if a setting is being used by any source

        Args:
            setting_name (str): the name of the setting

        Returns:
            bool: return true if the setting is being used, false otherwise
        """
        src_with_set = self.source_manager.get_sources_with_setting(setting_name)
        if len(src_with_set) == 0 : 
            return False 
        else:
            return True
    
    def remove_setting_from_source(self, source_name: str) -> bool:
        """ given a source name, remove the current setting from the source, 
            set the setting of the source to default

        Args:
            source_name (str): the name that identifies the source

        Returns:
            bool: return true if the setting is removed successfully false otherwise
        """
        return self.apply_setting_to_source(
            source_name, DEFAULT_SETTING_NAME, True)
    
    def get_plugin_setting(self, name: str):
        """ returns the plugin setting of the setting

        Args:
            setting_name (str): name that identifies a setting

        Returns:
            Union[bool, Dict[str, str]]: if the setting is found, return the 
            list of string that identifies which plugins are used, else return 
            false
        """
        setting: SettingObject = self.setting_manager.get_setting(name)
        if setting:
            return setting.get_plugin_setting()
        else:
            return False
    
    def get_configured_sources(self, sources : List[str] = None) -> List[SourceObject]:
        """ given the  a list of source name, return a list of the sourceObject
            that stores the source configured with setting
        Args:
            sources (List[str], optional): a list of source name, if not 
            given, return a list of configured source. Defaults to None.

        Returns:
            List[SourceObject]: a list of source object that stores the source data 
        """
        return self.source_manager.get_configured_sources(sources)
   
    def get_engine_setting_names(self) -> List[str]: 
        """ get a list of available engine setting name

        Returns:
            List[str]: the list of engine setting name
        """
        return self.setting_manager.get_engine_setting_names()
    
    def add_new_engine(self, name, setting, overwrite = False) -> bool:
        """ add a new engine setting 

        Args:
            name (str): the name of the engine setting
            setting (Dict[str, str]): the setting data stored in a dictionary
            overwrite (bool, optional): if True, overwrite the existing 
                                        engine setting with the same name. Defaults to False.

        Returns:
            bool: return True if the engine setting is successfully created
        """
        return self.setting_manager.add_new_engine(name, setting, overwrite)

    def remove_engine_setting(self, name) -> bool:
        """remove the engine setting identified by nanme

        Args:
            name (str): the name of the engine setting to be removed

        Returns:
            bool:  return True if the engine setting is successfully removed
        """
        return self.setting_manager.remove_engine_setting(name)
    
    def update_engine_setting(self, name, setting_data: Dict[str, str]) -> bool:
        """update the engine setting identified by name 

        Args:
            name (str): the name of the engine setting to be updated
            setting_data (Dict[str, str]): the content of the new setting

        Returns:
            bool:  return True if the engine setting is successfully updated 
        """
        return self.setting_manager.update_engine_setting(name, setting_data)
    
    def is_engine_setting(self, name: str):
        """check if the given engine name is engine setting

        Args:
            name (str): the name of the engine setting
        """
        return self.setting_manager.is_engine_setting(name)
     
    def get_engine_setting_data(self, name:str) -> Union[bool, Dict[str, str]]:
        """ get the enigine setting data 

        Args:
            name (str): the name of the engine setting

        Returns:
            Union[bool, Dict[str, str]]: if the engine setting name is available 
            return the engine setting data as stored in a dictionary, else return False
        """
        return self.setting_manager.get_engine_setting_data(name)
    
    def is_engine_setting_in_use(self, name:str) -> bool:
        """ check if the engine setting identified by name is in use

        Args:
            name (str): the name of the engine setting

        Returns:
            bool: return true if the engine setting is in use, false other wise
        """
        return self.setting_manager.is_engine_setting_in_use(name)
     
    def remove_all_settings(self) -> bool:
        """ remove all settings except for the default setting

        Returns:
            bool: return true if the removal is successful 
        """
        try:
            for setting in self.setting_manager.get_setting_names():
                if setting != DEFAULT_SETTING_NAME:
                    assert self.remove_setting(setting)

            for source in self.source_manager.get_configured_sources():
                assert source.setting_name() == DEFAULT_SETTING_NAME
            return True
        except Exception as e:
            logger.error(e, exc_info=e)
            return False
    
    def get_setting_names(self) -> List[str]:
        """ return a list of available setting names 

        Returns:
            List[str]: a list of available setting names
        """
        return self.setting_manager.get_setting_names()
    
    def get_all_settings_data(self) -> Dict[str, SettingDict]:
        """ 
        return a dictionary that stores all setting data
        """
        return self.setting_manager.get_all_settings_data()

    def get_all_profile_names(self) -> List[str]:
        """ 
        return a list of string that stores all setting name
        """
        return self.setting_manager.get_setting_names()
    
    def get_default_engine_setting_name(self) -> str:
        """ get the default setting name

        Returns:
            str: a string that represent the default setting
        """
        return self.setting_manager.get_default_engine_setting_name()
   
   
    def get_default_profile_setting_name(self) -> str:
        """ get the default setting name

        Returns:
            str: a string that represent the default setting
        """
        return self.setting_manager.get_default_profile_setting_name()
    
    
    def set_default_setting(self, setting_name:str) -> bool:
        """ set the default setting to setting_name

        Args:
            setting_name (str)
            
        Returns:
            bool:return true if the setting can be set, false otherwise
        """
        return self.setting_manager.set_to_default_setting(setting_name)
    
    def set_default_engine(self, engine_name:str) -> bool:
        """ set the default setting to engine_name

        Args:
            engine_name (str)
            
        Returns:
            bool:return true if the setting can be set, false otherwise
        """
        return self.setting_manager.set_to_default_engine_setting(engine_name)
    
    def is_suite_in_use(self, suite_name:str) -> bool:
        """given a suite_name, check if this suite is used 
           in any of the setting

        Args:
            suite_name (str): the name of the plugin suite

        Returns:
            bool: return true if the suite is used in any of the setting, 
                  false otherwise
        """
        return self.setting_manager.is_suite_in_use(suite_name)
    
    
    def get_profile_src_path(self, name: str):
        """get the  path to the profile setting source

        Args:
            name (str): the name of the profile 
        """
        return self.setting_manager.get_profile_src_path(name)


    def get_engine_src_path(self, name: str):
        """get the  path to the engine setting source

        Args:
            name (str): the name of the engine 
        """
        return self.setting_manager.get_engine_src_path(name)