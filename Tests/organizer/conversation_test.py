# Standard library imports
from datetime import date
# Local imports
from Src.Components.io import IO
from Src.Components.organizer import ConversationBuilder, SettingsBuilder,\
                                    Conversation

############################### GLOBALS #####################################
WAV_FILE_PATH = "TestData/media/test2a.wav"
RESULT_DIR_PATH = "TestData"
TMP_DIR_PATH = "TestData/workspace"
CONVERSATION_DIR_PATH = "TestData/media/conversation"

############################### SETUP #####################################

def build_valid_conversation_from_directory() -> Conversation:
    settings_builder = SettingsBuilder()
    data = {
        "sample_attribute_1" : None,
        "sample_attribute_2" : None}
    _,settings = settings_builder.create_settings(data)
    builder = ConversationBuilder(IO())
    builder.set_conversation_source_path(CONVERSATION_DIR_PATH)
    builder.set_conversation_name("conversation_dir")
    builder.set_result_directory_path(TMP_DIR_PATH)
    builder.set_temporary_directory_path(TMP_DIR_PATH)
    builder.set_number_of_speakers(2)
    builder.set_conversation_settings(settings)
    builder.build_conversation()
    return builder.get_conversation()

def build_valid_conversation_from_file() -> Conversation:
    settings_builder = SettingsBuilder()
    data = {
        "sample_attribute_1" : None,
        "sample_attribute_2" : None}
    _,settings = settings_builder.create_settings(data)
    builder = ConversationBuilder(IO())
    builder.set_conversation_source_path(WAV_FILE_PATH)
    builder.set_conversation_name("conversation_file")
    builder.set_result_directory_path(TMP_DIR_PATH)
    builder.set_temporary_directory_path(TMP_DIR_PATH)
    builder.set_number_of_speakers(2)
    builder.set_conversation_settings(settings)
    builder.build_conversation()
    return builder.get_conversation()



########################## TEST DEFINITIONS #################################

def test_conversation_get_conversation_name() -> None:
    """
    Tests the get_conversation_name method of Conversation object returned by
    ConversationBuilder.

    Tests:
        1. Check value of the returned name.

     Returns:
        (bool): True if all tests pass. False otherwise.
    """
    conversation_dir = build_valid_conversation_from_directory()
    conversation_file = build_valid_conversation_from_file()
    assert conversation_dir.get_conversation_name() == "conversation_dir" and \
        conversation_file.get_conversation_name() == "conversation_file"

def test_conversation_get_conversation_size() -> None:
    """
    Tests the get_conversation_size method of Conversation object returned by
    ConversationBuilder.

    Tests:
        1. Check value of the returned size.

     Returns:
        (bool): True if all tests pass. False otherwise.
    """
    io = IO()
    conversation_dir = build_valid_conversation_from_directory()
    conversation_file = build_valid_conversation_from_file()
    assert conversation_dir.get_conversation_size() == \
            io.get_size(CONVERSATION_DIR_PATH)[1] and \
        conversation_file.get_conversation_size() == io.get_size(WAV_FILE_PATH)[1]

def test_conversation_get_source_type() -> None:
    """
    Tests the get_source_type method of Conversation object returned by
    ConversationBuilder.

    Tests:
        1. Check value of the returned types.

     Returns:
        (bool): True if all tests pass. False otherwise.
    """
    conversation_dir = build_valid_conversation_from_directory()
    conversation_file = build_valid_conversation_from_file()
    assert conversation_dir.get_source_type() == "directory" and \
        conversation_file.get_source_type() == "file"

def test_conversation_get_transcription_date() -> None:
    """
    Tests the get_transcription_date method of Conversation object returned by
    ConversationBuilder.

    Tests:
        1. Make sure the date is a valid date object.

     Returns:
        (bool): True if all tests pass. False otherwise.
    """
    conversation_dir = build_valid_conversation_from_directory()
    conversation_file = build_valid_conversation_from_file()
    assert conversation_dir.get_transcription_date() == date.today() and \
        conversation_file.get_transcription_date() == date.today()

def test_conversation_get_transcription_status() -> None:
    """
    Tests the get_transcription_status method of Conversation object returned by
    ConversationBuilder.

    Tests:
        1. Make sure the status is ready in both cases.

     Returns:
        (bool): True if all tests pass. False otherwise.
    """
    conversation_dir = build_valid_conversation_from_directory()
    conversation_file = build_valid_conversation_from_file()
    assert conversation_dir.get_transcription_status() == "ready" and \
        conversation_file.get_transcription_status() == "ready"

def test_conversation_get_transcription_time() -> None:
    """
    Tests the get_transcription_times method of Conversation object returned by
    ConversationBuilder.

    Tests:
        1. Make sure the time is valid.

     Returns:
        (bool): True if all tests pass. False otherwise.
    """
    conversation_dir = build_valid_conversation_from_directory()
    conversation_file = build_valid_conversation_from_file()
    assert type(conversation_dir.get_transcription_time()) == str and \
        type(conversation_dir.get_transcription_time()) == str

def test_conversation_number_of_source_files() -> None:
    """
    Tests the number_of_source_files method of Conversation object returned by
    ConversationBuilder.

    Tests:
        1. Make sure the numbder of files is valid.

     Returns:
        (bool): True if all tests pass. False otherwise.
    """
    io = IO()
    conversation_dir = build_valid_conversation_from_directory()
    conversation_file = build_valid_conversation_from_file()
    assert conversation_dir.number_of_source_files() == \
            io.number_of_files_in_directory(CONVERSATION_DIR_PATH,["*"],False)[1] and \
        conversation_file.number_of_source_files() == 1

def test_conversation_number_of_speakers() -> None:
    """
    Tests the number_of_speakers method of Conversation object returned by
    ConversationBuilder.

    Tests:
        1. Make sure the numbder of speakers is valid.

     Returns:
        (bool): True if all tests pass. False otherwise.
    """
    conversation_dir = build_valid_conversation_from_directory()
    conversation_file = build_valid_conversation_from_file()
    assert conversation_dir.number_of_speakers() == 2 and \
        conversation_file.number_of_speakers() == 2

def test_conversation_get_source_file_names() -> None:
    """
    Tests the get_source_file_names of Conversation object returned by
    ConversationBuilder.

    Tests:
        1. Make sure the names are valid.

     Returns:
        (bool): True if all tests pass. False otherwise.
    """
    io = IO()
    dir_paths = io.path_of_files_in_directory(CONVERSATION_DIR_PATH,["*"],False)[1]
    dir_names = [io.get_name(path) for path in dir_paths]
    conversation_dir = build_valid_conversation_from_directory()
    conversation_file = build_valid_conversation_from_file()
    assert conversation_dir.get_source_file_names() == dir_names and \
        conversation_file.get_source_file_names() == [io.get_name(WAV_FILE_PATH)]

def test_conversation_get_source_file_paths() -> None:
    """
    Tests the get_source_file_paths of Conversation object returned by
    ConversationBuilder.

    Tests:
        1. Make sure the paths are valid.

     Returns:
        (bool): True if all tests pass. False otherwise.
    """
    io = IO()
    dir_paths = io.path_of_files_in_directory(CONVERSATION_DIR_PATH,["*"],False)[1]
    dir_names = [io.get_name(path) for path in dir_paths]
    conversation_dir = build_valid_conversation_from_directory()
    conversation_file = build_valid_conversation_from_file()
    assert list(conversation_dir.get_source_file_paths().values()) == dir_paths and \
        list(conversation_dir.get_source_file_paths().keys()) == dir_names and \
        list(conversation_file.get_source_file_paths().values()) == [WAV_FILE_PATH] and \
        list(conversation_file.get_source_file_paths().keys()) == [io.get_name(WAV_FILE_PATH)]

def test_conversation_get_source_file_types() -> None:
    """
    Tests the get_source_file_types of Conversation object returned by
    ConversationBuilder.

    Tests:
        1. Make sure the types are valid.

    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    conversation_dir = build_valid_conversation_from_directory()
    conversation_file = build_valid_conversation_from_file()
    assert list(conversation_dir.get_source_file_types().values()) == ["audio","audio"] and \
        list(conversation_file.get_source_file_types().values()) == ["audio"]
