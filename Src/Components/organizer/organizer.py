# Standrad library imports
from typing import Tuple, Dict, Any, Callable
# Local imports
from .conversation_builder import ConversationBuilder
from .conversation import Conversation
from .settings_builder import SettingsBuilder
from .settings import Settings

from ..io import IO
# Third party imports


class Organizer:
    """
    Responsible for managing Conversation and Settings objects.
    """

    def __init__(self, io: IO) -> None:
        """
        Args:
            io (IO): Initialized IO object.
        """
        # Objects
        self.io = io
        self.conversation_builder = ConversationBuilder(io)
        self.settings_builder = SettingsBuilder()

    # Settings methods

    def register_settings_type(self, settings_type: str,
                               setting_creator: Callable[[], Settings]) -> bool:
        """
        Register a new type of settings if it is not already registered.

        Args:
            settings_type (str): Type of the new settings.
            settings_creator (Callable[[],Settings])

        Returns:
            (bool):
                True if successful. False otherwise or if settings_type
                was previously registered.
        """
        return self.settings_builder.register_setting_type(
            settings_type, setting_creator)

    def get_registered_settings_types(self) -> Dict[str, Settings]:
        """
        Obtain a mapping from the settings type to creator

        Returns:
            (Dict[str,Settings]): Mapping from settings type to creator.
        """
        return self.settings_builder.get_registered_setting_types()

    def create_settings(self, settings_type: str,
                        data: Dict[str, Any]) -> Tuple[bool, Settings]:
        """
        Create a settings object with thr given data.

        Args:
            data (Data[str,Any]):
                Mapping from ALL SettingsAttributes as strings to their
                values.

        Returns:
            (Tuple[bool,Settings]):
                True + settings object if successful.
                False + None if unsuccessful.
        """
        return self.settings_builder.create_settings(settings_type, data)

    def copy_settings(self, settings: Settings) -> Settings:
        """
        Copy the given settings object.

        Args:
            settings (Settings): Object to copy.

        Returns:
            (Settings): Copy of the given object.
        """
        return self.settings_builder.copy_settings(settings)

    def change_settings(self, settings: Settings, data: Dict[str, Any]) \
            -> bool:
        """
        Change some or all of the attributes of the settings object with the
        given data.

        Args:
            settings (Settings): Object whose data is to be changed.
            data (Dict[str,Any]):
                Mapping from some SettingsAttributes to their associated values.

        Returns:
            (bool): True if successfully changed. False otherwise.
        """
        return self.settings_builder.change_settings(settings, data)

    # Conversation methods

    def create_conversation(self, source_path: str, conversation_name: str,
                            num_speakers: int, transcriber_name: str,
                            result_dir_path: str, temp_dir_path: str,
                            settings: Settings) -> Tuple[bool, Conversation]:
        """
        Creates a Conversation.

        Args:
            source_path (str):
                Path of the source from which the conversation is to be loaded,
                which can be a file or a directory.
            conversation_name (str):
                Set the name for the conversation that is to be created.
                The name simply acts as the unique identifier for the
                conversation.
            num_speakers (int):
                Set the number of speakers that are part of this conversation.
                Must be at least 1.
            transcriber_name (str): Name of the transcriber
            result_dir_path (str):
                Path to the final result directory. The directory must exist.
            temp_dir_path (str):
                Path to the temporary workspace directory.
                The directory must exist.
            settings (Settings): Settings for this conversation.

        Returns:
            (Tuple[bool,Conversation]):
                True + initialized conversaton object.
                False + None otherwise.
        """
        self.conversation_builder.clear_conversation_configurations()
        self.conversation_builder.set_conversation_source_path(source_path)
        self.conversation_builder.set_conversation_name(conversation_name)
        self.conversation_builder.set_number_of_speakers(num_speakers)
        self.conversation_builder.set_transcriber_name(transcriber_name)
        self.conversation_builder.set_result_directory_path(result_dir_path)
        self.conversation_builder.set_temporary_directory_path(temp_dir_path)
        self.conversation_builder.set_conversation_settings(settings)
        success = self.conversation_builder.build_conversation()
        return (success, self.conversation_builder.get_conversation())

    def apply_settings_to_conversation(self, conversation: Conversation,
                                       settings: Settings) -> Conversation:
        """
        Apply the settings to the given conversation object.

        Args:
            conversation (Conversation)
            settings (Settings)

        Returns:
            (Conversation): Conversation object with the settings applied.
        """
        # Internally creates a new Conversation object with different Settings.
        source_path = conversation.get_source_path()
        conversation_name = conversation.get_conversation_name()
        num_speakers = conversation.number_of_speakers()
        transcriber_name = conversation.get_transcriber_name()
        result_dir_path = conversation.get_result_directory_path()
        temp_dir_path = conversation.get_temp_directory_path()
        _, conversation = self.create_conversation(
            source_path, conversation_name, num_speakers, transcriber_name, result_dir_path,
            temp_dir_path, settings)
        return conversation
