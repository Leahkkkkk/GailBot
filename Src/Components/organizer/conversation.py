# Standard library imports
from typing import List, Dict
# Local imports
from .meta import Meta, MetaAttributes
from .data import DataFile, DataFileAttributes, DataFileTypes
from .settings import Settings
from .paths import Paths, PathsAttributes
from ..engines import Utterance
# Third party imports

class Conversation:
    """
    Responsible for sotring all relevant information about a conversation.
    """

    def __init__(self, meta : Meta, data_files : List[DataFile],
            settings : Settings, paths : Paths) -> None:
        """
        Args:
            meta (Meta): Contains all meta-data about the conversation.
            data_files (List[DataFile]):
                List of all data files in the conversation.
            settings (Settings):
                Transcription processes settings for the conversation.
            paths (Paths):
                Contains all file paths relevant to the overall conversation.
        """
        self.meta = meta
        self.data_files = data_files
        self.settings = settings
        self.paths = paths

    ################################## GETTERS ##############################

    ### Meta

    def get_conversation_name(self) -> str:
        """
        Obtain the name associated with this conversation

        Returns:
            (str): Name of the conversation.
        """
        return self.meta.get(MetaAttributes.conversation_name)[1]

    def get_conversation_size(self) -> bytes:
        """
        Obtain the total size of the input files to the conversation.

        Returns:
            (bytes): Size of all input files in bytes.
        """
        return self.meta.get(MetaAttributes.total_size_bytes)[1]

    def get_source_type(self) -> str:
        """
        Obtain the type of the source for this conversation.
        Can be either 'file' or 'directory'.

        Returns:
            (str): Type of the source for conversation.
        """
        return self.meta.get(MetaAttributes.source_type)[1]

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
        return self.meta.get(MetaAttributes.transcription_date)[1]

    def get_transcription_status(self) -> str:
        """
        Obtain the status of the status of the conversation in the
        transcription process.
        """
        return self.meta.get(MetaAttributes.transcription_status)[1]

    def get_transcription_time(self) -> str:
        """
        Obtain the time at which the transcription process was started.
        Note that this does not mean that the entire transcription
        process was completed.
        The time format is: HH:MM:SS

        Results (str): Time the transcription process was started.
        """
        return self.meta.get(MetaAttributes.transcription_time)[1]

    def get_transcriber_name(self) -> str:
        """
        Get the name of the transcriber.

        Returns:
            (str): Transcriber name
        """
        return self.meta.get(MetaAttributes.transcriber_name)[1]

    def number_of_source_files(self) -> int:
        """
        Obtain the number of source files for this conversation.

        Returns:
            (int): Number of source files.
        """
        return self.meta.get(MetaAttributes.num_data_files)[1]

    def number_of_speakers(self) -> int:
        """
        Obtain the number of speakers in the conversation.

        Returns:
            (int): Number of speakers in the conversation.
        """
        return self.meta.get(MetaAttributes.num_speakers)[1]


    ### DataFile

    def get_source_file_names(self) -> List[str]:
        """
        Obtain the name of all source files, not the path or the extension.

        Returns:
            (List[str]): Name of all source files.
        """
        return [data_file.get(DataFileAttributes.name)[1] for data_file \
            in self.data_files]

    def get_source_file_paths(self) -> Dict[str,str]:
        """
        Obtain the original paths of all source files.

        Returns:
            (Dict[str,str]): Mapping from source file names to paths.
        """
        data = dict()
        for data_file in self.data_files:
            name = data_file.get(DataFileAttributes.name)[1]
            path = data_file.get(DataFileAttributes.path)[1]
            data[name] = path
        return data

    def get_source_file_types(self) -> Dict[str,str]:
        """
        Obtain the type of each source file in the conversation.
        Can be either 'audio' or 'video'

        Returns:
            (Dict[str,str]):
                Mapping from source file name to its type.
        """
        data = dict()
        for data_file in self.data_files:
            name = data_file.get(DataFileAttributes.name)[1]
            file_type = data_file.get(DataFileAttributes.file_type)[1]
            if file_type == DataFileTypes.audio:
                data[name] = 'audio'
            else:
                data[name] = 'video'
        return data

    ### Settings

    def get_settings(self) -> Settings:
        """
        Obtain the settings object associated with the conversation.

        Returns:
            (Settings)
        """
        return self.settings

    ### Paths

    def get_result_directory_path(self) -> str:
        """
        Obtain the path to the directory designated as the final output
        directory for this conversation.

        Returns:
            (str): Final output directory path for conversation.
        """
        return self.paths.get(PathsAttributes.result_dir_path)[1]

    def get_source_path(self) -> str:
        """
        Obtain the source path, which can be either a file path or a directory
        path, for the whole conversation.

        Returns:
            (str): Source path for the conversation.
        """
        return self.paths.get(PathsAttributes.source_path)[1]

    def get_temp_directory_path(self) -> str:
        """
        Obtain the path to a directory assigned as the temporary workspace
        for this conversation.

        Returns:
            (str): Temporary directory path for this conversation.
        """
        return self.paths.get(PathsAttributes.temp_dir_path)[1]

    ################################ SETTERS ################################

    def set_transcription_status(self, status : str) -> bool:
        return self.meta.set(MetaAttributes.transcription_status,status)

    def set_number_of_speakers(self, num_speakers : int) -> bool:
        return self.meta.set(MetaAttributes.num_speakers,num_speakers)

    def set_utterances(self, utterance_map : Dict[str,List[Utterance]]) -> bool:
        file_names = self.get_source_file_names()
        if not all([name in file_names for name in utterance_map.keys()]):
            return False
        for data_file in self.data_files:
            data_file.set(DataFileAttributes.utterances,
                utterance_map[data_file.get(DataFileAttributes.name)])
        return True
