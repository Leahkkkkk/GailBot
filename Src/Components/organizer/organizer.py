# Standrad library imports
from typing import Tuple, Dict, Any, Callable, List
# Local imports
from .conversation import Conversation
from .settings import Settings
from .settings_builder import SettingsBuilder
from .conversation_builder import ConversationBuilder, ConversationCreator
from ..io import IO
# Third party imports


class Organizer:
    """
    Responsible for managing Conversation and Settings objects.
    """

    def __init__(self, io: IO) -> None:
        self.io = io
        self.conversation_builder = ConversationBuilder()
        self.settings_builder = SettingsBuilder()

    # --------  Settings methods

    def register_settings_type(self, settings_type: str,
                               setting_creator: Callable[[], Settings]) -> bool:
        return self.settings_builder.register_setting_type(
            settings_type, setting_creator)

    def remove_registered_settings_type(self, settings_type: str) -> None:
        return self.settings_builder.remove_registered_settings_type(
            settings_type)

    def is_registered_settings_type(self, settings_type: str) -> bool:
        return self.settings_builder.is_registered_settings_type(settings_type)

    def get_registered_settings_types(self) -> Dict[str, Settings]:
        return self.settings_builder.get_registered_setting_types()

    def create_settings(self, settings_type: str,
                        data: Dict[str, Any]) -> Tuple[bool, Settings]:
        return self.settings_builder.create_settings(settings_type, data)

    def copy_settings(self, settings: Settings) -> Settings:
        return self.settings_builder.copy_settings(settings)

    def change_settings(self, settings: Settings, data: Dict[str, Any]) \
            -> bool:
        return self.settings_builder.change_settings(settings, data)

    # ---------- Conversation methods

    def register_creator(self, name: str, creator: ConversationCreator) -> None:
        return self.conversation_builder.register_creator(name, creator)

    def remove_creator(self, name: str) -> None:
        return self.conversation_builder.remove_creator(name)

    def is_creator(self, name: str) -> bool:
        return self.conversation_builder.is_creator(name)

    def create_conversation(self, creator_name: str, creator_args: List,
                            creator_kwargs: Dict, settings: Settings)\
            -> Tuple[bool, Conversation]:
        return self.conversation_builder.build_conversation(
            creator_name, creator_args, creator_kwargs, settings)

    # --------- Settings and Conversation methods
    def apply_settings_to_conversation(self, conversation: Conversation,
                                       settings: Settings) -> Conversation:
        if settings.is_configured():
            conversation.settings = settings
            return conversation
