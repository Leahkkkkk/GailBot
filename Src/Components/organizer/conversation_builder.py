# Standard library imports
from typing import List, Dict, Tuple
from copy import deepcopy
from datetime import datetime, date
from abc import ABC, abstractmethod
# Local imports
from .settings import Settings
from .conversation import Conversation, Meta, DataFile, Paths
from ..io import IO


class ConversationCreator(ABC):

    @abstractmethod
    def configure(self, *args, **kwargs) -> bool:
        pass

    @abstractmethod
    def create_meta(self) -> Meta:
        pass

    @abstractmethod
    def create_data_files(self) -> List[DataFile]:
        pass

    @abstractmethod
    def create_paths(self) -> Paths:
        pass


class ConversationBuilder:

    def __init__(self) -> None:
        self.io = IO()
        self.creators = dict()

    def register_creator(self, name: str, creator: ConversationCreator) -> None:
        self.creators[name] = creator

    def remove_creator(self, name: str) -> None:
        if self.is_creator(name):
            del self.creators[name]

    def is_creator(self, name: str) -> bool:
        return name in self.creators

    def build_conversation(self, creator_name: str, configure_args: List,
                           configure_kwargs: Dict, settings: Settings) \
            -> Tuple[bool, Conversation]:
        if not self.is_creator(creator_name):
            return (False, None)

        try:
            creator: ConversationCreator = self.creators[creator_name]()
            if not creator.configure(*configure_args, **configure_kwargs):
                return (False, None)
            data_files = creator.create_data_files()
            meta = creator.create_meta()
            paths = creator.create_paths()
            conv = Conversation(
                meta, data_files, settings, paths)
            return (True, conv)
        except Exception as e:
            print("Exception!", e)
            return (False, None)
