# Standard imports
from abc import ABC, abstractmethod
# Local imports
from ..fs_service import FileSystemService
from ....organizer import Organizer, Conversation
from ....engines import Utterance, UtteranceAttributes
from ....io import IO
from .source import Source


class SourceLoader(ABC):

    def __init__(self, fs_service: FileSystemService,
                 organizer: Organizer) -> None:
        self.fs_service = fs_service
        self.organizer = organizer

    @abstractmethod
    def load_source(self, source_name: str, source_path: str,
                    result_dir_path: str, transcriber_name: str) -> Source:
        pass
