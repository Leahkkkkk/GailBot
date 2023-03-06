from typing import Dict, List, Any, Tuple, Union
from .organizer import Organizer, SettingDict
from .converter import Converter 
from .pipeline import PipelineService
from ..plugins import PluginManager, PluginSuite
from gailbot.core.utils.logger import makelogger
from gailbot.workspace.manager import WorkspaceManager

""" TODO: plugin vs. plugin suite naming """
NUM_THREAD = 5
logger = makelogger("service_controller")
""" Knows about all three sub modules """
class ServiceController:
    def __init__(self, ws_manager: WorkspaceManager, load_exist_setting: bool = False) -> None:
        self.organizer = Organizer(ws_manager.setting_src, load_exist_setting)
        self.converter = Converter(ws_manager)
        self.plugin_manager = PluginManager(ws_manager.plugin_src)
        self.pipeline_service = PipelineService(
            self.plugin_manager, num_threads = NUM_THREAD) 
    
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
            logger.error(e)
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
        logger.info(self.organizer.get_configured_sources())
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
     
    def get_engine_setting(self, setting_name: str) -> Union[bool, Dict[str, str]]:
        """ given a setting name, return its engine setting 

        Args:
            setting_name (str): the name that identifies the setting

        Returns:
            Dict[str, str]: 
            if the setting is found, returns the engine setting that is 
            stored in a dictionary, else return false
        """
        return self.organizer.get_engine_setting(setting_name)
    
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

    def transcribe(self, sources: List[str] = None) -> Tuple [bool, List[str]]:
        """ return a list of file that was not able to be transcribed, 
            and the transcription result of the rest of the file

        Args:
            sources (List[str], optional): _description_. Defaults to None.

        Returns:
            List[str]: _description_
        """
        # get configured sources 
        try:
            if not sources:
                sources = self.organizer.get_configured_sources(sources)
            else: 
                sources = [self.organizer.get_source(name) for name in sources]
            # load to converter 
            payloads, invalid = self.converter(sources)
            if len(sources) != 0:
                logger.info(payloads)
                # put the payload to the pipeline
                result = self.pipeline_service(payloads=payloads)
                logger.info(f"the transcription result is {result}")
                logger.info(f"the invalid files are {invalid}")
            else:
                result = False
            return result, invalid
        except Exception as e:
            logger.error(e)
            return False, []
        
    def register_plugin_suite(self, plugin_source: str) -> str:
        return self.plugin_manager.register_suite(plugin_source)
        
    def get_plugin(self, suite_name) -> PluginSuite:
        return self.plugin_manager.get_suite(suite_name)
    
    def is_plugin(self, suite_name: str) -> bool:
        return self.plugin_manager.is_suite(suite_name)
    
    def delete_plugin(self, suite_name: str) -> bool:
        return self.plugin_manager.delete_suite(suite_name)
     