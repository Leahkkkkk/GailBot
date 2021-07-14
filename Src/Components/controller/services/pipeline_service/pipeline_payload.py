# Standard library imports
from typing import Dict, Any, List
from copy import deepcopy
# Local imports
from ....organizer import Conversation
from ....plugin_manager import PluginExecutionSummary
from ..organizer_service import Source, RequestType

class SourcePayload:
    """
    Adapter class for the pipeline.
    """

    def __init__(self, source : Source) -> None:
        self.source : Source = source
        self.transcription_successful : bool = False
        self.analysis_successful : bool = False
        self.format_successful : bool = False
        self.source_to_audio_map : Dict[str,str] = dict()
        self.analysis_plugin_summaries : Dict[str, PluginExecutionSummary]\
            = dict()
        self.format_plugin_summaries : Dict[str,PluginExecutionSummary] \
            = dict()

    ################################# MODIFIERS ###############################

    def add_to_source(self, identifier : str, path : str,
            item_type : str, copy : bool = False) -> bool:
        return self.source.get_hook().add_to_source(
            identifier, path,item_type,copy)

    def remove_from_source(self, identifier : str) -> bool:
        return self.source.get_hook().remove_from_source(identifier)

    def write_to_file(self, identifier : str, item_type : str, file_name : str,
            extension : str, data : Any, overwrite : bool = False) -> bool:
        return self.source.get_hook().write_to_file(
            identifier, item_type, file_name, extension, data, overwrite)

    def save_to_directory(self) -> bool:
        return self.source.get_hook().save_to_directory()

    def log(self, request_type : RequestType, request : str) -> None:
        self.source.log(request_type, request)

    ############################### GETTERS ###################################

    def get_source(self) -> Source:
        return self.source

    def get_source_name(self) -> str:
        return self.source.get_source_name()

    def get_conversation(self) -> Conversation:
        return self.source.get_conversation()

    def change_item_type(self, identifier : str, new_item_type : str) -> bool:
        return self.source.get_hook().change_item_type(
            identifier, new_item_type)

    def is_contained(self, identifier : str) -> bool:
        return self.source.get_hook().is_contained(identifier)

    def get_workspace_path(self) -> str:
        return self.source.get_hook().get_workspace_path()

    def get_result_directory_path(self) -> str:
        return self.source.get_hook().get_result_directory_path()

    def get_output_names(self) -> List[str]:
        paths = list(self.source.get_hook().get_hooked_paths("permanent").values())
        return [path[path.rfind("/")+1:] for path in paths]

    def is_transcribed(self) -> bool:
        return self.transcription_successful

    def is_analyzed(self) -> bool:
        return self.analysis_successful

    def is_formatted(self) -> bool:
        return self.format_successful

    def get_analysis_plugin_summaries(self) -> Dict[str,PluginExecutionSummary]:
        return deepcopy(self.analysis_plugin_summaries)

    def get_format_plugin_summaries(self) -> Dict[str,PluginExecutionSummary]:
        return deepcopy(self.format_plugin_summaries)

    def get_source_to_audio_map(self) -> Dict[str,str]:
        return deepcopy(self.source_to_audio_map)

    ############################### SETTERS ###################################

    def set_transcription_status(self, is_successful : bool) -> None:
        self.transcription_successful = is_successful

    def set_analysis_status(self, is_successful : bool) -> None:
        self.analysis_successful = is_successful

    def set_format_status(self, is_successful : bool) -> None:
        self.format_successful = is_successful

    def set_analysis_plugin_summaries(self,
            summaries : Dict[str,PluginExecutionSummary]) -> None:
        self.analysis_plugin_summaries = summaries

    def set_format_plugin_summaries(self,
            summaries : Dict[str,PluginExecutionSummary]) -> None:
        self.format_plugin_summaries = summaries

    def set_source_to_audio_map(self, source_to_audio_map : Dict[str,str]) \
            -> None:
        self.source_to_audio_map = source_to_audio_map
