
# Local imports
from Src.Components.organizer import Meta, MetaAttributes

############################### GLOBALS #####################################

########################## TEST DEFINITIONS #################################

def test_create_meta_valid() -> None:
    """
    Tests the Meta object.

    Tests:
        1. Create a meta object with valid data and determine if it is
            configured.

    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    data = {
        "conversation_name" : "test_conversation",
        "total_size_bytes" : 0,
        "num_data_files" : 0,
        "source_type" : "file",
        "transcription_date" : None,
        "transcription_status" : "not_transcribed",
        "transcription_time" : None,
        "total_speakers" : 1}
    meta = Meta(data)
    assert meta.is_configured()

def test_create_meta_invalid() -> None:
    """
    Tests the Meta object.

    Tests:
        1. Create a meta object with invalid data and determine if it is
            configured.

    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    data_1 = {
        "conversation_name" : "test_conversation",
        "total_size_bytes" : 0,
        "num_data_files" : 0,
        "source_type" : "file",
        "transcription_date" : None,
        "transcription_status" : "not_transcribed",
        "transcription_time" : None,
        "total_speakers" : 1}
    data_2 = {
        "conversation_name" : "test_conversation"}
    data_3 = {
        "conversation_name" : "test_conversation",
        "total_size_bytes" : 0,
        "num_data_files" : 0,
        "source_type" : "file",
        "transcription_date" : None,
        "transcription_status" : "not_transcribed",
        "transcription_time" : None,
        "total_speakers" : 1,
        "extra" : None}
    meta_1 = Meta(data_1)
    meta_2 = Meta(data_2)
    meta_3 = Meta(data_3)
    assert meta_1.is_configured() and \
        not meta_2.is_configured() and \
        not meta_3.is_configured()

def test_create_meta_invalid_missing_keys() -> None:
    """
    Tests the Meta object.

    Tests:
        1. Create a meta object with invalid missing data and determine if it is
            configured.

    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    data = {
        "conversation_name" : "test_conversation"}
    meta = Meta(data)
    assert not meta.is_configured()

def test_create_meta_invalid_extra_keys() -> None:
    """
    Tests the Meta object.

    Tests:
        1. Create a meta object with invalid extra data and determine if it is
            configured.

    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    data = {
        "conversation_name" : "test_conversation",
        "total_size_bytes" : 0,
        "num_data_files" : 0,
        "source_type" : "file",
        "transcription_date" : None,
        "transcription_status" : "not_transcribed",
        "transcription_time" : None,
        "total_speakers" : 1,
        "extra" : None}
    meta = Meta(data)
    assert not meta.is_configured()

def test_create_meta_invalid_empty() -> None:
    """
    Tests the Meta object.

    Tests:
        1. Create a meta object with invalid empty data and determine if it is
            configured.

    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    data = {}
    meta = Meta(data)
    assert not meta.is_configured()

def test_meta_get_valid() -> None:
    """
    Tests the get method in Meta.

    Tests:
        1. Get a valid attribute

    Returns:
        (bool): True if all tests pass. False otherwise
    """
    data = {
        "conversation_name" : "test_conversation",
        "total_size_bytes" : 0,
        "num_data_files" : 0,
        "source_type" : "file",
        "transcription_date" : None,
        "transcription_status" : "not_transcribed",
        "transcription_time" : None,
        "total_speakers" : 1}
    meta = Meta(data)
    assert meta.get(MetaAttributes.conversation_name)[1] == "test_conversation" and \
        meta.get(MetaAttributes.total_size_bytes)[1] == 0 and \
        meta.get(MetaAttributes.total_speakers)[1] == 1 and \
        meta.get(MetaAttributes.source_type)[1] == "file" and \
        meta.get(MetaAttributes.transcription_status)[1] =="not_transcribed" and \
        meta.get(MetaAttributes.transcription_date)[1] == None and \
        meta.get(MetaAttributes.transcription_time)[1] == None

def test_meta_get_invalid() -> None:
    """
    Tests the get method in Meta.

    Tests:
        1. Get a invalid attribute

    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    data = {
        "conversation_name" : "test_conversation",
        "total_size_bytes" : 0,
        "num_data_files" : 0,
        "source_type" : "file",
        "transcription_date" : None,
        "transcription_status" : "not_transcribed",
        "transcription_time" : None,
        "total_speakers" : 1}
    meta = Meta(data)
    assert not meta.get("invalid")[0]

def test_meta_set_valid() -> None:
    """
    Test the set method in Meta

    Tests:
        1. Set a valid attribute and check result.

    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    data = {
        "conversation_name" : "test_conversation",
        "total_size_bytes" : 0,
        "num_data_files" : 0,
        "source_type" : "file",
        "transcription_date" : None,
        "transcription_status" : "not_transcribed",
        "transcription_time" : None,
        "total_speakers" : 1}
    meta = Meta(data)
    assert meta.set(MetaAttributes.total_speakers, 10) and \
        meta.get(MetaAttributes.total_speakers)[1] == 10

def test_meta_set_invalid() -> None:
    """
    Test the set method in Meta.

    Tests:
        1. Set an invalid attribute and check results.
        2. Set an invalid type for file_type.

    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    data = {
        "conversation_name" : "test_conversation",
        "total_size_bytes" : 0,
        "num_data_files" : 0,
        "source_type" : "file",
        "transcription_date" : None,
        "transcription_status" : "not_transcribed",
        "transcription_time" : None,
        "total_speakers" : 1}
    meta = Meta(data)
    assert not meta.set("invalid", None)