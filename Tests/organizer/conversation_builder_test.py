# Standard library imports
from typing import Dict, Any
# Local imports
from Src.Components.io import IO
from Src.Components.organizer import ConversationBuilder, Settings, \
    SettingsBuilder, Conversation
from Tests.organizer.vardefs import *

############################### GLOBALS #####################################

############################### SETUP #######################################


class CustomSettings(Settings):

    ATTRS = ("attr_1", "attr_2")

    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(attrs=self.ATTRS)
        self._parse_data(data)

    def get_attr_1(self) -> Any:
        return self.get("attr_1")[1]

    def get_attr_2(self) -> Any:
        return self.get("attr_2")[1]

    def _parse_data(self, data: Dict[str, Any]) -> bool:
        if not all([k in data.keys() for k in self.ATTRS]):
            return False
        for k, v in data.items():
            self._set_value(k, v)
        return True


def build_settings(data: Dict[str, Any]) -> Settings:
    builder = SettingsBuilder()
    builder.register_setting_type("custom", lambda data: CustomSettings(data))
    _, settings = builder.create_settings("custom", data)
    return settings

########################## TEST DEFINITIONS #################################


def test_builder_set_conversation_source_path_valid() -> None:
    """
    Tests the set_conversation_source_path method in ConversationBuilder

    Tests:
        1. Set a valid file path.
        2. Set a valid directory path.

    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    builder = ConversationBuilder(IO())
    assert builder.set_conversation_source_path(WAV_FILE_PATH) and \
        builder.set_conversation_source_path(CONVERSATION_DIR_PATH)


def test_builder_set_conversation_source_path_invalid() -> None:
    """
    Tests the set_conversation_source_path method in ConversationBuilder

    Tests:
        1. Set an invalid path.

    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    builder = ConversationBuilder(IO())
    assert not builder.set_conversation_source_path("Not a path")


def test_builder_set_conversation_name() -> None:
    """
    Tests the set_conversation_name method in ConversationBuilder

    Tests:
        1. Set any random name.

    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    builder = ConversationBuilder(IO())
    assert builder.set_conversation_name("conversation_1")


def test_builder_set_result_directory_path_valid() -> None:
    """
    Tests the set_result_directory_path method in ConversationBuilder

    Tests:
        1. Set a valid directory path.

    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    builder = ConversationBuilder(IO())
    assert builder.set_result_directory_path(TMP_DIR_PATH)


def test_builder_set_result_directory_path_invalid() -> None:
    """
    Tests the set_result_directory_path method in ConversationBuilder

    Tests:
        1. Set a file path as directory.
        2. Set an invalid path.

    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    builder = ConversationBuilder(IO())
    assert not builder.set_result_directory_path(WAV_FILE_PATH) and \
        not builder.set_result_directory_path("invalid/")


def test_builder_set_temporary_directory_path_valid() -> None:
    """
    Tests the set_temporary_directory_path method in ConversationBuilder

    Tests:
        1. Set a valid directory path.

    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    builder = ConversationBuilder(IO())
    assert builder.set_temporary_directory_path(TMP_DIR_PATH)


def test_builder_set_temporary_directory_path_invalid() -> None:
    """
    Tests the set_temporary_directory_path method in ConversationBuilder

    Tests:
        1. Set a file path as directory.
        2. Set an invalid path.

    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    builder = ConversationBuilder(IO())
    assert not builder.set_temporary_directory_path(WAV_FILE_PATH) and \
        not builder.set_temporary_directory_path("invalid/")


def test_builder_set_conversation_name() -> None:
    """
    Tests the set_conversation_name method in ConversationBuilder

    Tests:
        1. Set a name and check if it can be obtained in the conversation.
    """
    builder = ConversationBuilder(IO())
    assert builder.set_conversation_name("conversation_name")


def test_builder_set_transcriber_name() -> None:
    """
    Tests the set_transcriber_name method in ConversationBuilder

    Tests:
        1. Set a name and check if it can be obtained in the conversation.
    """
    builder = ConversationBuilder(IO())
    assert builder.set_transcriber_name("conversation_name")


def test_builder_set_number_of_speakers_valid() -> None:
    """
    Tests the set_number_of_speakers method in ConversationBuilder

    Tests:
        1. Set a positive number of speakers.

    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    builder = ConversationBuilder(IO())
    assert builder.set_number_of_speakers(10)


def test_builder_set_number_of_speakers_invalid() -> None:
    """
    Tests the set_number_of_speakers method in ConversationBuilder

    Tests:
        1. Set 0 as number of speakers.
        2. Set a negative number of speakers.

    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    builder = ConversationBuilder(IO())
    assert not builder.set_number_of_speakers(0) and \
        not builder.set_number_of_speakers(-10)


def test_builder_set_conversation_settings_valid() -> None:
    """
    Tests the set_conversation_settings method in ConversationBuilder

    Tests:
        1. Set a settings object that has all attributes set.

    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    data = {
        "attr_1": 1,
        "attr_2": 2
    }
    settings = build_settings(data)
    builder = ConversationBuilder(IO())
    assert builder.set_conversation_settings(settings)


def test_builder_set_conversation_settings_invalid() -> None:
    """
    Tests the set_conversation_settings method in ConversationBuilder

    Tests:
        1. Set a settings object that is not configured.

    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    data = {
        "attr_1": None}
    settings = Settings(data.keys())
    builder = ConversationBuilder(IO())
    assert not builder.set_conversation_settings(settings)


def test_builder_build_conversation_valid() -> None:
    """
    Tests the build_conversation method in ConversationBuilder

    Tests:
        1. Call method after setting all attributes with valid data.

    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    data = {
        "attr_1": 1,
        "attr_2": 2}
    settings = build_settings(data)
    builder = ConversationBuilder(IO())
    builder.set_conversation_source_path(CONVERSATION_DIR_PATH)
    builder.set_conversation_name("conversation_1")
    builder.set_result_directory_path(TMP_DIR_PATH)
    builder.set_temporary_directory_path(TMP_DIR_PATH)
    builder.set_number_of_speakers(2)
    builder.set_transcriber_name("NAME")
    builder.set_conversation_settings(settings)
    assert builder.build_conversation()


def test_builder_build_conversation_invalid() -> None:
    """
    Tests the build_conversation method of ConversationBuilder.

    Tests:
        1. Build a conversation without setting any attributes.
        2. Build a conversation after setting only some attributes.
        3. Build a conversation after clearing configurations.
        4. Build a conversation after building a valid conversation.

    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    data = {
        "attr_1": 1,
        "attr_2": 2}
    settings = build_settings(data)
    builder = ConversationBuilder(IO())
    assert not builder.build_conversation()
    assert builder.get_conversation() == None
    assert builder.set_conversation_source_path(CONVERSATION_DIR_PATH)
    assert builder.set_conversation_name("only some attributes set")
    assert not builder.build_conversation()
    assert builder.get_conversation() == None
    assert builder.clear_conversation_configurations()
    assert builder.set_conversation_source_path(CONVERSATION_DIR_PATH)
    assert builder.set_conversation_name("conversation_1")
    assert builder.set_result_directory_path(TMP_DIR_PATH)
    assert builder.set_temporary_directory_path(TMP_DIR_PATH)
    assert builder.set_number_of_speakers(2)
    assert builder.set_transcriber_name("NAME")
    assert builder.set_conversation_settings(settings)
    assert builder.build_conversation()
    assert builder.get_conversation() != None
    assert builder.clear_conversation_configurations()
    assert not builder.build_conversation()
    assert builder.get_conversation() == None


def test_builder_clear_conversation() -> None:
    """
    Tests the builder clear conversation method

    Tests:
        1. Builds conversation
        2. Clear conversation
        3. Confirms conversation is cleared with a get

    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    data = {
        "attr_1": 1,
        "attr_2": 2}
    settings = build_settings(data)
    builder = ConversationBuilder(IO())
    builder.set_conversation_source_path(CONVERSATION_DIR_PATH)
    builder.set_conversation_name("conversation_1")
    builder.set_result_directory_path(TMP_DIR_PATH)
    builder.set_temporary_directory_path(TMP_DIR_PATH)
    builder.set_number_of_speakers(2)
    builder.set_conversation_settings(settings)
    builder.build_conversation()
    assert builder.clear_conversation_configurations() and\
        builder.get_conversation() == None
