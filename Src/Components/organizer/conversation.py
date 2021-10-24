# Standard library imports
from typing import List, Dict
from dataclasses import dataclass
from datetime import datetime
from abc import ABC
# Local imports
from .settings import Settings


@dataclass
class DataFile:
    name: str = None
    extension: str = None
    file_type: str = None
    path: str = None
    size_bytes: str = None
    utterances: List = None


@dataclass
class Meta:
    conversation_name: str = None
    total_size_bytes: bytes = None
    num_data_files: int = None
    source_type: str = None
    transcription_date: datetime = None
    transcription_time: datetime = None
    transcriber_name: str = None
    num_speakers: int = None


@dataclass
class Paths:
    result_dir_path: str = None
    source_path: str = None
    temp_dir_path: str = None


class Conversation:

    def __init__(self, meta: Meta, data_files: List[DataFile],
                 settings: Settings, paths: Paths):
        self.meta = meta
        self.data_files = data_files
        self.settings = settings
        self.paths = paths

    def get_conversation_name(self) -> str:
        """
        Obtain the name associated with this conversation

        Returns:
            (str): Name of the conversation.
        """
        return self.meta.conversation_name

    def get_conversation_size(self) -> bytes:
        """
        Obtain the total size of the input files to the conversation.

        Returns:
            (bytes): Size of all input files in bytes.
        """
        return self.meta.total_size_bytes

    def get_source_type(self) -> str:
        """
        Obtain the type of the source for this conversation.
        Can be either 'file' or 'directory'.

        Returns:
            (str): Type of the source for conversation.
        """
        return self.meta.source_type

    def get_transcription_date(self) -> str:
        """
        Obtain the date the transcription process was started on this
        conversation.
        Note that this does not mean that the entire transcription
        process was completed.

        Returns:
            (str):
                Date the transcription process was started on the conversation.
        """
        return self.meta.transcription_date

    def get_transcription_time(self) -> str:
        """
        Obtain the time at which the transcription process was started.
        Note that this does not mean that the entire transcription
        process was completed.
        The time format is: HH:MM:SS

        Results (str): Time the transcription process was started.
        """
        return self.meta.transcription_time

    def get_transcriber_name(self) -> str:
        """
        Get the name of the transcriber.

        Returns:
            (str): Transcriber name
        """
        return self.meta.transcriber_name

    def number_of_source_files(self) -> int:
        """
        Obtain the number of source files for this conversation.

        Returns:
            (int): Number of source files.
        """
        return self.meta.num_data_files

    def number_of_speakers(self) -> int:
        """
        Obtain the number of speakers in the conversation.

        Returns:
            (int): Number of speakers in the conversation.
        """
        return self.meta.num_speakers

    # DataFile

    def get_source_file_names(self) -> List[str]:
        """
        Obtain the name of all source files, not the path or the extension.

        Returns:
            (List[str]): Name of all source files.
        """
        return [data_file.name for data_file in self.data_files]

    def get_source_file_paths(self) -> Dict[str, str]:
        """
        Obtain the original paths of all source files.

        Returns:
            (Dict[str,str]): Mapping from source file names to paths.
        """
        data = dict()
        for data_file in self.data_files:
            name = data_file.name
            path = data_file.path
            data[name] = path
        return data

    def get_source_file_types(self) -> Dict[str, str]:
        """
        Obtain the type of each source file in the conversation.
        Can be either 'audio' or 'video'

        Returns:
            (Dict[str,str]):
                Mapping from source file name to its type.
        """
        data = dict()
        for data_file in self.data_files:
            name = data_file.name
            file_type = data_file.file_type
            data[name] = file_type
        return data

    def get_utterances(self) -> Dict[str, List]:
        """
        Get a mapping from the name of the data file to a list of utterances.

        Returns:
            utterance_map (Dict[str,List[Utterance]]):
                Map from name of data file to a list of its utterances.
        """
        utterance_map = dict()
        for data_file in self.data_files:
            utterance_map[data_file.name] = data_file.utterances
        return utterance_map

    # Settings

    def get_settings(self) -> Settings:
        """
        Obtain the settings object associated with the conversation.

        Returns:
            (Settings)
        """
        return self.settings

    # Paths

    def get_result_directory_path(self) -> str:
        """
        Obtain the path to the directory designated as the final output
        directory for this conversation.

        Returns:
            (str): Final output directory path for conversation.
        """
        return self.paths.result_dir_path

    def get_source_path(self) -> str:
        """
        Obtain the source path, which can be either a file path or a directory
        path, for the whole conversation.

        Returns:
            (str): Source path for the conversation.
        """
        return self.paths.source_path

    def get_temp_directory_path(self) -> str:
        """
        Obtain the path to a directory assigned as the temporary workspace
        for this conversation.

        Returns:
            (str): Temporary directory path for this conversation.
        """
        return self.paths.temp_dir_path

    ################################ SETTERS ################################

    def set_number_of_speakers(self, num_speakers: int) -> bool:
        """
        Set the number of speakers in the conversation.

        Args:
            num_speakers (int): Cannot be less than 1.

        Returns:
            (bool): True if successfully set. False otherwise.
        """
        if num_speakers < 1:
            return False
        return self.meta.num_speakers

    def set_utterances(self, utterance_map: Dict[str, List]) -> bool:
        """
        Set the utterances for every data file.

        Args:
            utterance_map (Dict[str,List[Utterance]]):
                Map from name of data file to a list of its utterances.

        Returns:
            (bool): True if successfully set. False otherwise.
        """
        file_names = self.get_source_file_names()
        if not all([name in file_names for name in utterance_map.keys()]):
            return False
        for data_file in self.data_files:
            data_file.utterances = utterance_map[data_file.name]
        return True
