# Standard imports
from typing import List
from abc import ABC, abstractmethod
# Local imports
from ..fs_service import FileSystemService
from ...io import IO
from .objects import Source


class SourceLoader(ABC):

    @abstractmethod
    def load_source(self, source_name: str, source_path: str,
                    result_dir_path: str, transcriber_name: str) -> Source:
        pass


class FileSourceLoader(SourceLoader):

    def __init__(self, fs_service: FileSystemService) -> None:
        super().__init__()
        self.fs_service = fs_service
        self.io = IO()

    ################################# MODIFIERS #########################

    def load_source(self, source_name: str, source_path: str,
                    result_dir_path: str, transcriber_name: str) -> Source:
        # Determine if can load
        if not self._can_load_source(source_path):
            return
        # Generate the source hook.
        source_hook = self.fs_service.generate_source_hook(
            source_name, result_dir_path)
        if source_hook == None:
            return
        # Generate the source object
        return Source(source_name, source_path, transcriber_name, source_hook)

    ################################# PRIVATE METHODS #########################

    def _can_load_source(self, source_path: str) -> bool:
        # Must be file.
        if not self.io.is_file(source_path):
            return False
        # Must be supported.
        _, source_extension = self.io.get_file_extension(source_path)
        if not source_extension in self.io.get_supported_audio_formats() and \
                not source_extension in self.io.get_supported_video_formats():
            return False
        return True


class DirectorySourceLoader(SourceLoader):

    def __init__(self, fs_service: FileSystemService) -> None:
        super().__init__()
        self.fs_service = fs_service
        self.io = IO()

    def load_source(self, source_name: str, source_path: str,
                    result_dir_path: str, transcriber_name: str) -> Source:
        # Determine if can load
        if not self._can_load_source(source_path):
            return
        # Generate the source hook.
        source_hook = self.fs_service.generate_source_hook(
            source_name, result_dir_path)
        if source_hook == None:
            return
        return Source(source_name, source_path, transcriber_name, source_hook)

    def _can_load_source(self, source_path: str) -> bool:
        return self.io.is_directory(source_path)


class TranscribedSourceLoader(SourceLoader):
    def __init__(self, fs_service: FileSystemService) -> None:
        super().__init__()
        self.fs_service = fs_service
        self.io = IO()
        # Vars.
        self.metadata_file_name = "metadata"
        self.metadata_file_ext = "json"
        self.source_raw_transcription_extension = "gb_raw"

    def load_source(self, source_name: str, source_path: str,
                    result_dir_path: str, transcriber_name: str) -> Source:
        # Determine if can load
        if not self._can_load_source(source_path):
            return
        # Generate the source hook.
        source_hook = self.fs_service.generate_source_hook(
            source_name, result_dir_path)
        if source_hook == None:
            return

        # This means that everything has been checked and we can load!
        return Source(source_name, source_path, transcriber_name, source_hook)

    def _can_load_source(self, source_path: str) -> bool:
        """
        Only load the previous GailBot outputs
        """
        if not self.io.is_directory(source_path):
            return False
        # Check if the metadata file exists
        if not self._does_meta_exist(source_path):
            return False
        # Read the metatafile and use it to check other files
        meta_path = self._get_meta_path(source_path)
        did_read, meta_data = self.io.read(meta_path)
        if meta_path == None or not did_read:
            return False
        try:
            # The data should have been transcribed properly and
            # raw files should be there.
            return meta_data["is_transcribed"] and \
                self._check_raw_outputs(source_path, meta_data["outputs"])
        except Exception as e:
            return False

    def _check_raw_outputs(self, source_path, output_paths: List[str]) -> bool:
        raw_outputs = [path for path in output_paths if
                       self.io.get_file_extension(path)
                       == self.source_raw_transcription_extension]
        # Ensure that this matches the actual raw files.
        _, actual_paths = self.io.path_of_files_in_directory(
            source_path, [self.source_raw_transcription_extension], False)
        actual_names = [self.io.get_name(
            path) for path in actual_paths]
        for raw_output in raw_outputs:
            if not self.io.get_name(raw_output) in actual_names:
                return False
        return True

    def _get_meta_path(self, source_path: str) -> str:
        _, paths = self.io.path_of_files_in_directory(
            source_path, [self.metadata_file_ext], False)
        return [path for path in paths if self.io.get_name(
            path) == self.metadata_file_name][0]

    def _does_meta_exist(self, source_path: str) -> bool:
        _, paths = self.io.path_of_files_in_directory(
            source_path, [self.metadata_file_ext], False)
        return len([path for path in paths if self.io.get_name(
            path) == self.metadata_file_name]) > 0
