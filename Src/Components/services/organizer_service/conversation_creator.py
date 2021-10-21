
from typing import List
from datetime import datetime
from ...organizer import ConversationCreator, Settings, Meta, DataFile, Paths
from ...engines import Utterance, UtteranceAttributes
from ...io import IO


class CustomConversationCreator(ConversationCreator):

    def __init__(self) -> None:
        self.io = IO()

    def configure(self, source_path: str, conversation_name: str,
                  num_speakers: int, transcriber_name: str,
                  result_dir_path: str, temp_dir_path: str,
                  settings: Settings) -> bool:
        self.source_path = source_path
        self.conversation_name = conversation_name
        self.num_speakers = num_speakers
        self.transcriber_name = transcriber_name
        self.result_dir_path = result_dir_path
        self.temp_dir_path = temp_dir_path
        self.settings = settings
        self.data_files = None
        return True

    def create_meta(self) -> Meta:
        if self.data_files == None:
            raise Exception()
        # Collecting data from data files
        total_size_bytes = sum([data_file.size_bytes
                                for data_file in self.data_files])
        source_type = "file" if self.io.is_file(
            self.source_path) else "directory"
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        current_date = now.strftime("%m/%d/%Y")
        return Meta(
            self.conversation_name,
            total_size_bytes,
            len(self.data_files),
            source_type,
            current_date,
            current_time,
            self.transcriber_name,
            self.num_speakers)

    def create_data_files(self) -> List[DataFile]:
        data_files = list()
        # Simply create a data file for a file source.
        if self.io.is_file(self.source_path):
            data_files.append(
                self._initialize_data_file(self.source_path))
        # Get all the file paths in the directory and convert to data files.
        elif self.io.is_directory(self.source_path):
            # Supported formats include both audio and video.
            supported_formats = list(self.io.get_supported_audio_formats())
            supported_formats.extend(
                list(self.io.get_supported_video_formats()))
            # NOTE: Check - adding additional gb_raw format to look for
            supported_formats.append("gb_raw")
            _, file_paths = self.io.path_of_files_in_directory(
                self.source_path, supported_formats, False)
            for path in file_paths:
                data_files.append(
                    self._initialize_data_file(path))
        else:
            raise Exception()
        self.data_files = data_files
        return data_files

    def create_paths(self) -> Paths:

        return Paths(
            self.result_dir_path, self.source_path, self.temp_dir_path)

    def _initialize_data_file(self, source_file_path: str) -> DataFile:
        """
        Given a source file path, generates a DataFile object for this file.
        Raises ExceptionUnexpected if the DataFile object cannot be configured.

        Args:
            source_file_path (str): Path to a source file.

        Returns:
            (DataFile): object representing the file at the given path.
        """
        utterances = list()
        if not self.io.is_file(source_file_path):
            raise Exception()
        if self.io.is_supported_audio_file(source_file_path):
            file_type = "audio"
        elif self.io.is_supported_video_file(source_file_path):
            file_type = "video"
        # -- NOTE: Check - assing handler for gb_raw file here!
        elif self.io.get_file_extension(source_file_path)[1] == "gb_raw":
            # Parse the raw file
            # NOTE: The data file type needs to be changes / added maybe?
            file_type = "audio"
            data = open(source_file_path, "r").readlines()
            # print("Size", self.io.get_size(source_file_path))
            for line in data:
                tokens = line.split(" ")
                utt = Utterance(
                    {"speaker_label": tokens[0].rstrip(":"),
                     "start_time": float(tokens[2][:tokens[2].find("_")]),
                     "end_time": float(tokens[2][tokens[2].find("_")+1:].rstrip("/n")),
                     "transcript": tokens[1]})
                utterances.append(utt)
        else:
            raise Exception()
        return DataFile(
            self.io.get_name(source_file_path),
            self.io.get_file_extension(source_file_path)[1],
            file_type,
            source_file_path,
            self.io.get_size(source_file_path)[1],
            utterances)
