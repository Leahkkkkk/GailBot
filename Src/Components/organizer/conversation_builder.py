# Standard library imports
from typing import List
from copy import deepcopy
from datetime import datetime, date
# Local imports
from ...utils.exceptions import ExceptionInvalid, ExceptionUnexpected
from ..io import IO
from .conversation import Conversation
from .meta import Meta
from .data import DataFile, DataFileAttributes, DataFileTypes
from .settings import Settings
from .paths import Paths
# Third party imports


class ConversationBuilder:
    """
    Responsible for creating Conversation objects.
    """

    def __init__(self, io: IO) -> None:
        """
        Args:
            io (IO): Initialized instance of an IO object.
        """
        # Params
        self.io = io
        self.core_data = {
            "source_path": None,
            "conversation_name": None,
            "transcription_status": "ready",
            "transcriber_name": None,
            "result_dir_path": None,
            "temp_dir_path": None,
            "settings": None,
            "num_speakers": None}
        self.conversation = None

    ############################# PUBLIC METHODS #############################

    # GETTERS

    def get_conversation(self) -> Conversation:
        """
        Obtain a Conversation object. Intended to be called after
        build_conversation.

        Returns:
            (Conversation):
                Conversation object if conversation has been constructed.
                None if no conversation has been constructed.
        """
        return deepcopy(self.conversation)

    # SETTERS

    def set_conversation_source_path(self, source_path: str) -> bool:
        """
        Set the path of the source from which the conversation is to be loaded,
        which can be a file or a directory.

        Args:
            source_path (str): Path to the source file or directory.

        Returns:
            (bool): True if successfully set. False otherwise.
        """
        if not self.io.is_directory(source_path) and \
                not self.io.is_file(source_path):
            return False
        self.core_data["source_path"] = source_path
        return True

    def set_conversation_name(self, name: str) -> bool:
        """
        Set the name for the conversation that is to be created.
        The name simply acts as the unique identifier for the conversation.

        Args:
            name (str): Name for the conversation.

        Returns:
            (bool): True if successfully set. False otherwise.
        """
        self.core_data["conversation_name"] = name
        return True

    def set_transcriber_name(self, name: str) -> bool:
        """
        Set the name of the transcriber

        Args:
            name (str)

        Returns:
            (bool): True if successfully set. False otherwise.
        """
        self.core_data["transcriber_name"] = name
        return True

    def set_number_of_speakers(self, num_speakers: int) -> bool:
        """
        Set the number of speakers, which must be a non-negative value.

        Args:
            num_speakers (int)

        Returns:
            (bool): True if successfully set. False otherwise.
        """
        if num_speakers <= 0:
            return False
        self.core_data["num_speakers"] = num_speakers
        return True

    def set_result_directory_path(self, result_dir_path: str) -> bool:
        """
        Path to the final result directory. The directory must exist.

        Args:
            result_dir_path (str): Path to the final result

        Returns:
            (bool): True if successfully set. False otherwise.
        """
        if not self.io.is_directory(result_dir_path):
            return False
        self.core_data["result_dir_path"] = result_dir_path
        return True

    def set_temporary_directory_path(self, temp_dir_path: str) -> bool:
        """
        Path to the temporary workspace directory. The directory must exist.

        Args:
            temp_dir_path (str): Path to the final result

        Returns:
            (bool): True if successfully set. False otherwise.
        """
        if not self.io.is_directory(temp_dir_path):
            return False
        self.core_data["temp_dir_path"] = temp_dir_path
        return True

    def set_conversation_settings(self, settings: Settings) -> bool:
        """
        Set the settings object for this conversation.

        Args:
            settings (Settings)

        Returns:
            (bool): True if successfully set. False otherwise.
        """
        if not settings.is_configured():
            return False
        self.core_data["settings"] = settings
        return True

    # Others

    def clear_conversation_configurations(self) -> bool:
        """
        Clear all configurations that have been set using various setters.
        Generally used before building a new conversation.

        Returns:
            (bool):
                True if all attributes are successfully reset. False otherwise.
        """
        for k in self.core_data.keys():
            self.core_data[k] = None
        self.core_data["transcription_status"] = "ready"
        self.conversation = None
        return True

    def build_conversation(self) -> bool:
        """
        Build a Conversation object.
        All attributes MUST have been set using the provided setters.

        Returns:
            (bool):
                True if the conversation is successfully built. False otherwise.
        """
        if not self._is_ready_to_build():
            return False
        # Create the data file objects first.
        data_files = self._initialize_data_files(
            self.core_data["source_path"])
        # Use datafile objects to initialize Meta values.
        meta = self._initialize_meta(
            self.core_data["source_path"], self.core_data["conversation_name"],
            self.core_data["transcription_status"],
            self.core_data["transcriber_name"], self.core_data["num_speakers"],
            data_files)
        # Use data set by user to create paths object
        paths = self._initialize_paths(
            self.core_data["result_dir_path"], self.core_data["source_path"],
            self.core_data["temp_dir_path"])
        conversation = Conversation(
            meta, data_files, self.core_data["settings"], paths)
        self.conversation = conversation
        return True

    ############################# PRIVATE METHODS #############################

    def _is_ready_to_build(self) -> bool:
        """
        Returns True if the conversation is ready to be built after all
        attributes have been set.
        """
        return (all([v != None for v in self.core_data.values()]))

    def _initialize_data_files(self, source_path: str) -> List[DataFile]:
        """
        Given a source path that can be a file or a directory, initializes
        DataFile objects for every supported audio or video file at the
        source path.
        Raises ExceptionInvalid if the source_path is not a path to a file or
        directory.

        Args:
            source_path (str): Path to the source file or directory.

        Returns:
            (List[DataFile]):
                List of DataFile objects representing all supported audio
                or video files at the source.
        """
        data_files = list()
        # Simply create a data file for a file source.
        if self.io.is_file(source_path):
            data_files.append(
                self._initialize_data_file(source_path))
        # Get all the file paths in the directory and convert to data files.
        elif self.io.is_directory(source_path):
            # Supported formats include both audio and video.
            supported_formats = list(self.io.get_supported_audio_formats())
            supported_formats.extend(
                list(self.io.get_supported_video_formats()))
            _, file_paths = self.io.path_of_files_in_directory(
                source_path, supported_formats, False)
            for path in file_paths:
                data_files.append(
                    self._initialize_data_file(path))
        else:
            raise ExceptionInvalid
        return data_files

    def _initialize_data_file(self, source_file_path: str) -> DataFile:
        """
        Given a source file path, generates a DataFile object for this file.
        Raises ExceptionUnexpected if the DataFile object cannot be configured.

        Args:
            source_file_path (str): Path to a source file.

        Returns:
            (DataFile): object representing the file at the given path.
        """
        if not self.io.is_file(source_file_path):
            raise ExceptionInvalid()
        if self.io.is_supported_audio_file(source_file_path):
            file_type = DataFileTypes.audio
        elif self.io.is_supported_video_file(source_file_path):
            file_type = DataFileTypes.video
        else:
            raise ExceptionInvalid()
        data = {
            "name": self.io.get_name(source_file_path),
            "extension": self.io.get_file_extension(source_file_path)[1],
            "file_type": file_type,
            "path": source_file_path,
            "size_bytes": self.io.get_size(source_file_path)[1],
            "utterances": list()}
        data_file = DataFile(data)
        if not data_file.is_configured():
            raise ExceptionUnexpected
        return data_file

    def _initialize_meta(self, source_path: str, conversation_name: str,
                         transcription_status: str, transcriber_name: str,
                         num_speakers: int, data_files: List[DataFile]) -> Meta:
        """
        Creates a Meta object for the current conversation.
        Raises ExceptionUnexpected if the Meta object cannot be configured.

        Args:
            source_path (str):
                Path to the conversation source. Can be a file or directory.
            conversation_name (str): Name for the conversation.
            transcription_status (str): Status of the conversation.
            total_speakers (int)" Total number of speakers in the conversation.
            data_files (List[DataFile]):
                List of DataFile objects representing every supported files at
                the source.

        Returns:
            (Meta): Configured Meta class object.
        """
        # Collecting data from data files
        total_size_bytes = sum([data_file.get(DataFileAttributes.size_bytes)[1]
                                for data_file in data_files])
        source_type = "file" if self.io.is_file(source_path) else "directory"
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        current_date = now.strftime("%m/%d/%Y")
        data = {
            "conversation_name": conversation_name,
            "total_size_bytes": total_size_bytes,
            "num_data_files": len(data_files),
            "source_type": source_type,
            "transcription_date": current_date,
            "transcription_status": transcription_status,
            "transcription_time": current_time,
            "transcriber_name": transcriber_name,
            "num_speakers": num_speakers}
        meta = Meta(data)
        if not meta.is_configured():
            raise ExceptionUnexpected
        return meta

    def _initialize_paths(self, result_dir_path: str, source_path: str,
                          temp_dir_path: str) -> Paths:
        """
        Initializes a path object for the current conversation.

        Args:
            result_dir_path (str): Path to the resultant directroy.
            source_path (str):
                Path to the conversation source. Can be a file or directory.
            temp_dir_path (str): Path to temporary workspace for this conversation.

        Returns:
            (Paths): Configured paths object.
        """
        data = {
            "result_dir_path": result_dir_path,
            "source_path": source_path,
            "temp_dir_path": temp_dir_path}
        paths = Paths(data)
        if not paths.is_configured():
            raise ExceptionUnexpected
        return paths
