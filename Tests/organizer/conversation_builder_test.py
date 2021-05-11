
# Local imports
from Src.Components.io import IO
from Src.Components.organizer import ConversationBuilder, Settings, SettingsBuilder

############################### GLOBALS #####################################
WAV_FILE_PATH = "TestData/media/test2a.wav"
RESULT_DIR_PATH = "TestData"
TMP_DIR_PATH = "TestData/workspace"
CONVERSATION_DIR_PATH = "TestData/media/conversation"
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
        "sample_attribute_1" : None,
        "sample_attribute_2" : None}
    settings = Settings(data)
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
        "sample_attribute_1" : None}
    settings = Settings(data)
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
    settings_builder = SettingsBuilder()
    data = {
        "sample_attribute_1" : None,
        "sample_attribute_2" : None}
    _,settings = settings_builder.create_settings(data)
    builder = ConversationBuilder(IO())
    builder.set_conversation_source_path(CONVERSATION_DIR_PATH)
    builder.set_conversation_name("conversation_1")
    builder.set_result_directory_path(TMP_DIR_PATH)
    builder.set_temporary_directory_path(TMP_DIR_PATH)
    builder.set_number_of_speakers(2)
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
    settings_builder = SettingsBuilder()
    data = {
        "sample_attribute_1" : None,
        "sample_attribute_2" : None}
    _,settings = settings_builder.create_settings(data)
    builder = ConversationBuilder(IO())
    assert not builder.build_conversation() and \
        builder.get_conversation() == None and \
        builder.set_conversation_source_path(CONVERSATION_DIR_PATH) and \
        builder.set_conversation_name("only some attributes set") and \
        not builder.build_conversation() and \
        builder.get_conversation() == None and \
        builder.clear_conversation_configurations() and \
        builder.set_conversation_source_path(CONVERSATION_DIR_PATH) and \
        builder.set_conversation_name("conversation_1") and \
        builder.set_result_directory_path(TMP_DIR_PATH) and \
        builder.set_temporary_directory_path(TMP_DIR_PATH) and \
        builder.set_number_of_speakers(2) and \
        builder.set_conversation_settings(settings) and \
        builder.build_conversation() and \
        builder.get_conversation() != None and \
        builder.clear_conversation_configurations() and \
        not builder.build_conversation() and \
        builder.get_conversation() == None

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
    settings_builder = SettingsBuilder()
    data = {
        "sample_attribute_1" : None,
        "sample_attribute_2" : None}
    _,settings = settings_builder.create_settings(data)
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
