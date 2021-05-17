# Local imports
from Src.Components.organizer import DataFile, DataFileAttributes, DataFileTypes

############################### GLOBALS #####################################

########################## TEST DEFINITIONS #################################


def test_create_data_file_valid() -> None:
    """
    Tests the DataFile object.

    Tests:
        1. Create a paths object with valid data and determine if it is
            configured.

    Returns:
        (bool): True if all tests pass. False otherwise
    """
    data = {
        "name" : "test_name",
        "extension" : "wav",
        "file_type" : DataFileTypes.audio,
        "path" : "test_path",
        "size_bytes": 0,
        "utterances" : list()}
    data_file = DataFile(data)
    assert data_file.is_configured()


def test_create_data_file_invalid() -> None:
    """
    Tests the DataFile object.

    Tests:
        1. Create a paths object with invalid data and determine if it is
            configured.

    Returns:
        (bool): True if all tests pass. False otherwise
    """
    data_1 = {
        "name" : "test_name",
        "extension" : "wav",
        "file_type" : "blah",
        "path" : "test_path",
        "size_bytes": 0}
    data_2 = {
        "name" : "test_name"}
    data_3 = {
        "name" : "test_name",
        "extension" : "wav",
        "file_type" : "blach",
        "path" : "test_path",
        "size_bytes": 0,
        "extra" : None}
    data_file_1 = DataFile(data_1)
    data_file_2 = DataFile(data_2)
    data_file_3 = DataFile(data_3)
    assert not data_file_1.is_configured() and \
        not data_file_2.is_configured() and \
        not data_file_3.is_configured()

def test_create_data_file_invalid_bad_file_type() -> None:
    """
    Tests the DataFile object.

    Tests:
        1. Create a paths object with invalid bad file type data and
           determine if it is configured.

    Returns:
        (bool): True if all tests pass. False otherwise
    """
    data = {
        "name" : "test_name",
        "extension" : "wav",
        "file_type" : "blah",
        "path" : "test_path",
        "size_bytes": 0,
        "utterances" : list()}
    data_file = DataFile(data)
    assert not data_file.is_configured()

def test_create_data_file_invalid_missing_keys() -> None:
    """
    Tests the DataFile object.

    Tests:
        1. Create a paths object with invalid missing keys data and determine
           if it is configured.

    Returns:
        (bool): True if all tests pass. False otherwise
    """
    data = {
        "name" : "test_name"}
    data_file = DataFile(data)
    assert not data_file.is_configured()

def test_create_data_file_invalid_extra_keys() -> None:
    """
    Tests the DataFile object.

    Tests:
        1. Create a paths object with invalid extra keys data and
           determine if it is configured.

    Returns:
        (bool): True if all tests pass. False otherwise
    """
    data = {
        "name" : "test_name",
        "extension" : "wav",
        "file_type" : "blach",
        "path" : "test_path",
        "size_bytes": 0,
        "extra" : None}
    data_file = DataFile(data)
    assert not data_file.is_configured()

def test_create_data_file_invalid_empty() -> None:
    """
    Tests the DataFile object.

    Tests:
        1. Create a paths object with invalid empty data and determine if it is
            configured.

    Returns:
        (bool): True if all tests pass. False otherwise
    """
    data = {}
    data_file = DataFile(data)
    assert not data_file.is_configured()

def test_data_file_get_valid() -> None:
    """
    Tests the get method in DataFile.

    Tests:
        1. Get a valid attribute

    Returns:
        (bool): True if all tests pass. False otherwise
    """
    data = {
        "name" : "test_name",
        "extension" : "wav",
        "file_type" : DataFileTypes.audio,
        "path" : "test_path",
        "size_bytes": 0,
        "utterances" : list()}
    data_file = DataFile(data)
    assert data_file.get(DataFileAttributes.name)[1] == "test_name" and \
        data_file.get(DataFileAttributes.extension)[1] == "wav" and \
        data_file.get(DataFileAttributes.file_type)[1] == DataFileTypes.audio and \
        data_file.get(DataFileAttributes.path)[1] == "test_path" and \
        data_file.get(DataFileAttributes.size_bytes)[1] == 0

def test_data_file_get_invalid() -> None:
    """
    Tests the get method in DataFile.

    Tests:
        1. Get a invalid attribute

    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    data = {
        "name" : "test_name",
        "extension" : "wav",
        "file_type" : DataFileTypes.audio,
        "path" : "test_path",
        "size_bytes": 0,
        "utterances" : list()}
    data_file = DataFile(data)
    assert not data_file.get("invalid")[0]

def test_data_file_set_valid() -> None:
    """
    Test the set method in DataFile.

    Tests:
        1. Set a valid attribute and check result.

    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    data = {
        "name" : "test_name",
        "extension" : "wav",
        "file_type" : DataFileTypes.audio,
        "path" : "test_path",
        "size_bytes": 0,
        "utterances" : list()}
    data_file = DataFile(data)
    assert data_file.set(DataFileAttributes.name,"new_name") and \
        data_file.get(DataFileAttributes.name)[1] == "new_name"

def test_data_file_set_invalid() -> None:
    """
    Test the set method in DataFile.

    Tests:
        1. Set an invalid attribute and check results.
        2. Set an invalid type for file_type.

    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    data = {
        "name" : "test_name",
        "extension" : "wav",
        "file_type" : DataFileTypes.audio,
        "path" : "test_path",
        "size_bytes": 0,
        "utterances" : list()}
    data_file = DataFile(data)
    assert not data_file.set("invalid", None) and \
        not data_file.set(DataFileAttributes.file_type,"audio")

def test_data_file_set_invalid_bad_key() -> None:
    """
    Test the set method in DataFile.

    Tests:
        1. Set an invalid attribute and check results.

    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    data = {
        "name" : "test_name",
        "extension" : "wav",
        "file_type" : DataFileTypes.audio,
        "path" : "test_path",
        "size_bytes": 0,
        "utterances" : list()}
    data_file = DataFile(data)
    assert not data_file.set("invalid", None)

def test_data_file_set_invalid_file_type() -> None:
    """
    Test the set method in DataFile.

    Tests:
        1. Set an invalid type for file_type.

    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    data = {
        "name" : "test_name",
        "extension" : "wav",
        "file_type" : DataFileTypes.audio,
        "path" : "test_path",
        "size_bytes": 0,
        "utterances" : list()}
    data_file = DataFile(data)
    assert not data_file.set(DataFileAttributes.file_type,"audio") and \
        data_file.get(DataFileAttributes.file_type)[1] == DataFileTypes.audio
