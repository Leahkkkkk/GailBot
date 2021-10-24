
from typing import List, Dict
from datetime import datetime
from ...organizer import ConversationCreator, Settings, Meta, DataFile, Paths
from ...engines import Utterance, UtteranceAttributes
from ...io import IO


class CustomConversationCreator(ConversationCreator):

    def __init__(self) -> None:
        self.io = IO()
        self.data_files = None
        self.meta = None
        self.paths = None

    def configure(self, source_path: str, conversation_name: str,
                  transcriber_name: str, num_speakers: str,
                  result_dir_path: str, temp_dir_path: str,
                  data_file_configs: List[Dict]) -> bool:
        self.source_path = source_path
        self.conversation_name = conversation_name
        self.transcriber_name = transcriber_name
        self.num_speakers = num_speakers
        self.result_dir_path = result_dir_path
        self.temp_dir_path = temp_dir_path
        self.data_file_configs = data_file_configs
        # Create the data files using the configs
        self.data_files = self._create_data_files()
        self.meta = self._create_meta()
        self.paths = self._create_paths()
        return True

    def create_meta(self) -> Meta:
        return self.meta

    def create_data_files(self) -> List[DataFile]:
        return self.data_files

    def create_paths(self) -> Paths:
        return self.paths

    def _create_data_files(self) -> List[DataFile]:
        data_files = list()
        for config in self.data_file_configs:
            try:
                data_file = DataFile(
                    config["name"],
                    config["extension"],
                    config["file_type"],
                    config["path"],
                    config["size_bytes"],
                    config["utterances"])
                data_files.append(data_file)
            except Exception as e:
                print(e)
                return list()
        return data_files

    def _create_meta(self) -> Meta:
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

    def _create_paths(self) -> Paths:
        return Paths(
            self.result_dir_path, self.source_path, self.temp_dir_path)
