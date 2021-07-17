# Standard library imports
from typing import Dict, Any, List
from copy import deepcopy
# Local imports
from ....organizer import Conversation
from ....plugin_manager import PluginExecutionSummary
from ..organizer_service import Source, RequestType
from .payload_summary import PayloadSummary

class SourcePayload:
    """
    Adapter from a source object for use in the PipelineService.
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
        """
        Add an item with the specified identifier and path to the output
        for the specific source.
        Note that permanent types are added to final results while temporary
        and workspace types are not.

        Args:
            identifier (str): Unique identifier for the file or directory.
            path (str): Path to a file or directory.
            item_type (str): One of 'permanent', 'temporary', or 'workspace.
            copy (bool):
                If True, copies the file or directory, otherwise moves the
                file or directory.

        Returns:
            (bool): True if the item is successfully added, False otherwise.
        """
        return self.source.get_hook().add_to_source(
            identifier, path,item_type,copy)

    def remove_from_source(self, identifier : str) -> bool:
        """
        Remove an item with the specified identifier from the source.

        Args:
            identifier (str)

        Returns:
            (bool): True if removed, False otherwise.
        """
        return self.source.get_hook().remove_from_source(identifier)

    def write_to_file(self, identifier : str, item_type : str, file_name : str,
            extension : str, data : Any, overwrite : bool = False) -> bool:
        """
        Write a file with the specified identifier, file_name, extension,
        and data to the results for this specific source.

        Args:
            identifier (str): Unique identifier for the file or directory.
            file_name (str): Name of the file.
            extension (str): Extension of the file.
            overwrite (bool): If True, any existing file with the same name
                            or extension is overwritten.

        Returns:
            (bool): True if successfully written, False otherwise.
        """
        return self.source.get_hook().write_to_file(
            identifier, item_type, file_name, extension, data, overwrite)

    def save_to_directory(self) -> bool:
        """
        Write all permanent contents to the result directory for this source.

        Returns:
            (bool): True if all items successfully written, False otherwise.
        """
        return self.source.get_hook().save_to_directory()

    def log(self, request_type : RequestType, request : str) -> None:
        """
        Log a request with the request_type to this payload.

        Args:
            request_type (RequestType)
            request (str)
        """
        self.source.log(request_type, request)

    def generate_summary(self) -> PayloadSummary:
        """
        Generate a summary for this payload.

        Returns:
            (PayloadSummary)
        """
        return PayloadSummary(
            self.source.get_source_name(),
            self.source.get_settings_profile_name(),
            self.transcription_successful,
            self.analysis_successful,
            list(self.analysis_plugin_summaries.keys()),
            self.format_successful,
            list(self.format_plugin_summaries.keys()))

    ############################### GETTERS ###################################

    def get_source(self) -> Source:
        """
        Obtain the source associated with this payload.

        Returns:
            (Source)
        """
        return self.source

    def get_source_name(self) -> str:
        """
        Obtain the name of the source associated with this payload.
        """
        return self.source.get_source_name()

    def get_conversation(self) -> Conversation:
        """
        Obtain the conversation associated with this payload.
        """
        return self.source.get_conversation()

    def change_item_type(self, identifier : str, new_item_type : str) -> bool:
        """
        Change the type of the item associated with this identifier.
        """
        return self.source.get_hook().change_item_type(
            identifier, new_item_type)

    def is_contained(self, identifier : str) -> bool:
        """
        Determine if an item with the specified identifier is contained within
        this payload.

        Args:
            identifier (str)

        Returns:
            (bool): true if contained, False otherwise.
        """
        return self.source.get_hook().is_contained(identifier)

    def get_workspace_path(self) -> str:
        """
        Obtain the path to a workspace associated with this payload.
        """
        return self.source.get_hook().get_workspace_path()

    def get_result_directory_path(self) -> str:
        """
        Obtain the path to the result directory for this payload.
        """
        return self.source.get_hook().get_result_directory_path()

    def get_output_names(self) -> List[str]:
        """
        Obtain the names of all output of resultant files or directories
        for this payload.

        Returns:
            (List[str]): Identifier list.
        """
        paths = list(self.source.get_hook().get_hooked_paths("permanent").values())
        return [path[path.rfind("/")+1:] for path in paths]

    def is_transcribed(self) -> bool:
        """
        Determine if this payload has been transcribed.
        """
        return self.transcription_successful

    def is_analyzed(self) -> bool:
        """
        Determine if this payload has been analyzed.
        """
        return self.analysis_successful

    def is_formatted(self) -> bool:
        """
        Determine if this payload has been formatted.
        """
        return self.format_successful

    def get_analysis_plugin_summaries(self) -> Dict[str,PluginExecutionSummary]:
        """
        Obtain a summary for the analysis plugins executed for this payload.
        """
        return self.analysis_plugin_summaries

    def get_format_plugin_summaries(self) -> Dict[str,PluginExecutionSummary]:
        """
        Obtain a summary for the format plugins executed for this payload.
        """
        return self.format_plugin_summaries

    def get_source_to_audio_map(self) -> Dict[str,str]:
        """
        Obtain a mapping from source file names to paths of files that are
        their corresponding audio files.
        """
        return deepcopy(self.source_to_audio_map)

    ############################### SETTERS ###################################

    def set_transcription_status(self, is_successful : bool) -> None:
        """
        Set the transcription status.
        """
        self.transcription_successful = is_successful

    def set_analysis_status(self, is_successful : bool) -> None:
        """
        Set the analysis status.
        """
        self.analysis_successful = is_successful

    def set_format_status(self, is_successful : bool) -> None:
        """
        Set the format status.
        """
        self.format_successful = is_successful

    def set_analysis_plugin_summaries(self,
            summaries : Dict[str,PluginExecutionSummary]) -> None:
        """
        Set a summary for the analysis plugins executed for this payload.

        Args:
            summaries (Dict[str,PluginExecutionSummary])
        """
        self.analysis_plugin_summaries = summaries

    def set_format_plugin_summaries(self,
            summaries : Dict[str,PluginExecutionSummary]) -> None:
        """
        Set a summary for the format plugins executed for this payload.

        Args:
            summaries (Dict[str,PluginExecutionSummary])
        """
        self.format_plugin_summaries = summaries

    def set_source_to_audio_map(self, source_to_audio_map : Dict[str,str]) \
            -> None:
        """
        Set a mapping from source file names to paths of files that are
        their corresponding audio files.

        Args:
            source_to_audio_map (Dict[str,str])
        """
        self.source_to_audio_map = source_to_audio_map
