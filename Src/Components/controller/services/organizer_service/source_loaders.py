# Standard imports
from typing import List
# Local imports
from ..fs_service import FileSystemService
from ....organizer import Organizer, Conversation
from ....engines import Utterance,UtteranceAttributes
from ....io import IO
from ..status import TranscriptionStatus
from .source import Source
from .source_loader import SourceLoader

class FileSourceLoader(SourceLoader):

    def __init__(self, fs_service : FileSystemService,
            organizer : Organizer) -> None:
        super().__init__(fs_service,organizer)
        self.io = IO()

    ################################# MODIFIERS #########################

    def load_source(self, source_name : str, source_path : str,
            result_dir_path : str, transcriber_name : str) -> Source:
        # Determine if can load
        if not self._can_load_source(source_path):
            return
        # Generate the source hook.
        source_hook = self.fs_service.generate_source_hook(
            source_name,result_dir_path)
        if source_hook == None:
            return
        # Generate the source object
        return Source(source_name, source_path,transcriber_name, source_hook)

    ################################# PRIVATE METHODS #########################

    def _can_load_source(self, source_path : str) -> bool:
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

    def __init__(self, fs_service : FileSystemService,
            organizer : Organizer) -> None:
        super().__init__(fs_service,organizer)
        self.io = IO()
        ## Vars.
        self.metadata_file_name = "metadata"
        self.metadata_file_ext = "json"
        self.source_raw_transcription_extension = "gb_raw"

    def load_source(self, source_name : str, source_path : str,
            result_dir_path : str, transcriber_name : str) -> Source:
        # Determine if can load
        if not self._can_load_source(source_path):
            return
        # Generate the source hook.
        source_hook = self.fs_service.generate_source_hook(
            source_name,result_dir_path)
        if source_hook == None:
            return
        # Check if the source is pre-transcribed.
        if self._check_pretranscribed(source_path):
            # TODO: Add the ability to construct a Conversation object without
            # data files or using existing transcription.
            pass
        # Else return the normal source
        return Source(source_name, source_path,transcriber_name, source_hook)

    def _can_load_source(self, source_path : str) -> bool:
        return self.io.is_directory(source_path)

    def _check_pretranscribed(self, source_path : str) -> bool:
        # Check the metadata file.
        _, paths = self.io.path_of_files_in_directory(
            source_path,[self.metadata_file_ext],False)
        for path in paths:
            if self.io.get_name(path) == self.metadata_file_name:
                did_read, data = self.io.read(path)
                if not did_read:
                    return False
                try:
                    # Read transcription status flags and corresponding files.
                    if not data["is_transcribed"]:
                        return False
                    # Check the output files
                    raw_outputs = [path for path in data["outputs"] if \
                        self.io.get_file_extension(path)\
                            == self.source_raw_transcription_extension]
                    # Ensure that this matches the actual raw files.
                    _, actual_paths = self.io.path_of_files_in_directory(
                        source_path,[self.source_raw_transcription_extension,False])
                    actual_names = [self.io.get_name(path) for path in actual_paths]
                    for raw_output in raw_outputs:
                        if not self.io.get_name(raw_output) in actual_names:
                            return False
                    return True
                except:
                    return  False
        return False
