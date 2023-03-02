from typing import Dict, List, Any, Tuple
from .organizer import Organizer 
from .converter import Converter 
from .pipeline import PipelineService
from ..plugins import PluginManager, PluginSuite
from gailbot.core.utils.logger import makelogger

""" TODO: plugin vs. plugin suite naming """
logger = makelogger("service_controller")
""" Knows about all three sub modules """
class ServiceController:
    def __init__(self, load_exist_setting: bool = False) -> None:
        self.organizer = Organizer(load_exist_setting)
        self.converter = Converter()
        self.plugin_manager = PluginManager()
        self.pipeline_service = PipelineService(self.plugin_manager, num_threads=5) # TODO: add this to toml file
    
    def add_sources(self, src_output_pairs: List [Tuple [str, str]]):
        logger.info(src_output_pairs)
        try:
            for src_pair in src_output_pairs:
                (source_path, out_path) = src_pair
                logger.info(source_path)
                logger.info(out_path)
                assert self.add_source(source_path, out_path)
            return True
        except Exception as e:
            logger.error(e)
            return False
        
    def add_source(self, src_path: str, out_path: str) -> bool:
        logger.info(f"add source {src_path}")
        logger.info(self.organizer.get_configured_sources())
        return self.organizer.add_source(src_path, out_path)
        
    def remove_source(self, name: str) -> None:
        return self.organizer.remove_source(name)
    
    def is_source(self, name:str) -> bool:
        return self.organizer.is_source(name)
    
    def create_new_setting(self, name: str, setting: Dict[str, str]) -> bool:
        return self.organizer.create_new_setting(name, setting)
        
    def save_setting(self, setting_name: str) -> bool:
        return self.organizer.save_setting_profile(setting_name)
    
    def rename_setting(self, old_name: str, new_name: str) -> bool:
        return self.organizer.rename_setting(old_name, new_name)
    
    def update_setting(self, setting_name: str, new_setting: Dict[str, str]) -> bool:
        return self.organizer.update_setting(setting_name, new_setting)
    
    def get_engine_setting(self, setting_name: str) -> Dict[str, str]:
        return self.organizer.get_engine_setting(setting_name)
    
    def get_plugin_setting(self, setting_name: str) -> Dict[str, str]:
        return self.organizer.get_plugin_setting(setting_name)
    
    def remove_setting(self, setting_name: str) -> bool:
        return self.organizer.remove_setting(setting_name)
    
    def is_setting(
        self, name:str ) -> bool:
        return self.organizer.is_setting(name)
        
    def apply_setting_to_sources(
        self, sources: List[str], setting: str, overwrite: bool = True) -> bool:
        return self.organizer.apply_setting_to_sources(sources, setting, overwrite)
    
    def apply_setting_to_source(
        self, source: str, setting: str, overwrite: bool = True) -> bool:
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
     