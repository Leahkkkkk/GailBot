# Standard imports
from typing import List, Callable
from abc import ABC, abstractmethod
# Local imports
from ..fs_service import FileSystemService
from ...io import IO
from .objects import Source


class SourceLoader:

    def __init__(self, fs_service: FileSystemService) -> None:
        self.fs_service = fs_service
        self.io = IO()
        self.can_load_methods = list()

    ################################# MODIFIERS #########################

    def add_source_checker(self, can_load_method: Callable) -> None:
        self.can_load_methods.append(can_load_method)

    def load_source(self, source_name: str, source_path: str,
                    result_dir_path: str, transcriber_name: str) -> Source:
        # Check if the source can be loaded.
        if not any([can_load(source_path) for can_load in self.can_load_methods]):
            return
        # Generate the source hook.
        source_hook = self.fs_service.generate_source_hook(
            source_name, result_dir_path)
        if source_hook == None:
            return
        # This means that everything has been checked and we can load!
        return Source(source_name, source_path, transcriber_name, source_hook)
