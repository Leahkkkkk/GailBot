# Local imports
from Src.Components.organizer import Paths, PathsAttributes
from Tests.organizer.vardefs import *

############################### GLOBALS #####################################


########################## TEST DEFINITIONS #################################

def test_paths_create_valid_data() -> None:
    """
    Tests the paths object.

    Tests:
        1. Create a paths object with valid data and determine if it is
            configured.

    Returns:
        (bool): True if all tests pass. False otherwise
    """
    paths_data = {
        "result_dir_path": RESULT_DIR_PATH,
        "source_path": WAV_FILE_PATH,
        "data_file_paths": [],
        "temp_dir_path": TMP_DIR_PATH}
    paths = Paths(paths_data)
    assert paths.is_configured()


def test_paths_create_invalid_data() -> None:
    """
    Tests the paths object.

    Tests:
        1. Create a paths object with invalid data and determine if it is
            configured.

    Returns:
        (bool): True if all tests pass. False otherwise
    """
    paths_data = {
        "result_dir_path": RESULT_DIR_PATH,
        "source_path": WAV_FILE_PATH}
    paths = Paths(paths_data)
    assert not paths.is_configured()


def test_paths_get_valid() -> None:
    """
    Tests the get method of Paths

    Tests:
        1. Obtain a valid attribute data

    Returns:
        (bool): True if all tests pass. False otherwise
    """
    paths_data = {
        "result_dir_path": RESULT_DIR_PATH,
        "source_path": WAV_FILE_PATH,
        "data_file_paths": [],
        "temp_dir_path": TMP_DIR_PATH}
    paths = Paths(paths_data)
    assert paths.is_configured() and \
        paths.get(PathsAttributes.result_dir_path)[1] == RESULT_DIR_PATH and \
        paths.get(PathsAttributes.temp_dir_path)[1] == TMP_DIR_PATH


def test_paths_get_invalid() -> None:
    """
    Tests the get method of Paths

    Tests:
        1. Obtain an invalid attribute data

    Returns:
        (bool): True if all tests pass. False otherwise
    """
    paths_data = {
        "result_dir_path": RESULT_DIR_PATH,
        "source_path": WAV_FILE_PATH,
        "data_file_paths": [],
        "temp_dir_path": TMP_DIR_PATH}
    paths = Paths(paths_data)
    assert paths.is_configured() and \
        not paths.get("invalid")[0]
