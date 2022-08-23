# Standard library imports
import os
# Local imports
from Src.components.io import GeneralIO
from Tests.io.vardefs import *


############################### GLOBALS #####################################


########################## TEST DEFINITIONS ##################################


def test_general_io_is_directory() -> None:
    """
    Tests the is_directory method in GeneralIO

    Tests:
        1. Use on a valid directory.
        2. Use on an invalid directory

    Returns:
        (bool): True if successful. False otherwise.
    """
    general = GeneralIO()
    assert general.is_directory(TEST_DIR_PATH) and \
        not general.is_directory(WAV_FILE_1_PATH)


def test_general_io_is_file() -> None:
    """
    Tests the is_file method in GeneralIO

    Tests:
        1. Use on a valid file.
        2. Use on an invalid file

    Returns:
        (bool): True if successful. False otherwise.
    """
    general = GeneralIO()
    assert not general.is_file(TEST_DIR_PATH) and \
        general.is_file(WAV_FILE_1_PATH)


def test_general_io_num_files_in_directory() -> None:
    """
    Tests the number_of_files_in_directory method in GeneralIO

    Tests:
        1. Use on a valid directory path
        2. Use on an invalid directory path.
        3. Use valid extensions.
        4. Use the wildcard extension.
        5. Use invalid file extensions.
        6. Check subdirectories

    Returns:
        (bool): True if successful. False otherwise.
    """
    general = GeneralIO()
    assert general.number_of_files_in_directory(TEST_DIR_PATH)[1] == 0 and \
        not general.number_of_files_in_directory(WAV_FILE_1_PATH)[0] and \
        general.number_of_files_in_directory(MEDIA_TEST_DIR_PATH, ["avi"])[1] == 1 and \
        general.number_of_files_in_directory(TEST_DIR_PATH, [".asjkd.j"])[1] == 0 and \
        general.number_of_files_in_directory(
            TEST_DIR_PATH, ["avi"], True)[1] == 1


def test_general_io_path_of_files_in_directory() -> None:
    """
    Tests the names_of_files_in_directory method in GeneralIO

    Tests:
        1. Use on a valid directory path
        2. Use on an invalid directory path.
        3. Use valid extensions.
        4. Use the wildcard extension.
        5. Use invalid file extensions.
        6. Check subdirectories

    Returns:
        (bool): True if successful. False otherwise.
    """
    general = GeneralIO()
    assert general.path_of_files_in_directory(TEST_DIR_PATH)[0] and \
        not general.path_of_files_in_directory(WAV_FILE_1_PATH)[0] and \
        general.path_of_files_in_directory(TEST_DIR_PATH, ["pdf"])[0] and \
        general.number_of_files_in_directory(TEST_DIR_PATH, [".asjkd.j"])[1] == 0 and \
        general.number_of_files_in_directory(TEST_DIR_PATH, ["pdf"], True)[0]


def test_general_io_number_of_subdirectories() -> None:
    """
    Tests:
        1. Provide a valid directory.
        2. Provide a file path.
        3. Provide an invalid path.
    """
    general = GeneralIO()
    assert general.number_of_subdirectories(TEST_DIR_PATH)[1] > 0
    assert not general.number_of_subdirectories(WAV_FILE_1_PATH)[0]
    assert not general.number_of_subdirectories("invalid")[0]


def test_general_io_paths_of_subdirectories() -> None:
    """
    Tests:
        1. Provide a valid directory.
        2. Provide a file path.
        3. Provide an invalid path.
    """
    general = GeneralIO()
    assert all([general.is_directory(path) for path
                in general.paths_of_subdirectories(TEST_DIR_PATH)[1]])
    assert not general.paths_of_subdirectories(WAV_FILE_1_PATH)[0]
    assert not general.paths_of_subdirectories("invalid")[0]


def test_general_io_is_readable() -> None:
    """
    Tests the is_readbale method in general.

    Tests:
        1. Read a text file
        2. Read a json file
        3. Read a yaml file
        4. Should not read a wav file.
        5. Should not read a video file.
        6. Should not read a directory.

    Returns:
        (bool): True if successful. False otherwise.
    """
    general = GeneralIO()
    assert general.is_readable(VALID_SAMPLE_TXT_FILE) and \
        general.is_readable(VALID_SAMPLE_JSON_FILE) and \
        general.is_readable(VALID_SAMPLE_YAML_FILE) and \
        not general.is_readable(WAV_FILE_1_PATH) and \
        not general.is_readable(VIDEO_FILE_AVI_PATH) and \
        not general.is_readable(TEST_DIR_PATH)


def test_general_io_get_file_extension() -> None:
    """
    Tests the get file extension method in GeneralIO.

    Tests:
        1. Read a file and get extension.
        2. Try to get extension of a directory.

    Returns:
        (bool): True if successful. False otherwise.
    """
    general = GeneralIO()
    assert general.get_file_extension(WAV_FILE_1_PATH) == "wav" and \
        general.get_file_extension(TEST_DIR_PATH) == ""


def test_general_io_read_files() -> None:
    """
    Tests the read_file method in GeneralIO

    Tests:
        1. Read a valid json file.
        2. Read a text file.
        3. Read a yaml file.
        4. Read an invalid format.
        65 Read from an invalid file path.

    Returns:
        (bool): True if successful. False otherwise.
    """
    general = GeneralIO()
    assert general.read_file(VALID_SAMPLE_JSON_FILE,)[0] and \
        general.read_file(VALID_SAMPLE_TXT_FILE)[0] and \
        general.read_file(VALID_SAMPLE_YAML_FILE,)[0] and \
        not general.read_file(VIDEO_FILE_AVI_PATH)[0] and \
        not general.read_file(TEST_DIR_PATH)[0]


def test_general_io_read_files_custom_extension() -> None:
    """
    Tests:
        1. Read a file with a custom extension / format.
    """
    general = GeneralIO()
    # Make a unique extension file and read it.
    path = TEST_DIR_PATH + "/test_test.apple"
    general.write_to_file(path,
                          general.read_file(VALID_SAMPLE_TXT_FILE)[1], False)
    success, data = general.read_file(path)
    assert success
    assert data == general.read_file(VALID_SAMPLE_TXT_FILE)[1]


def test_general_io_write_to_file() -> None:
    """
    Tests the write_to_file method in GeneralIO

    Tests:
        1. Write a valid file in all types of supported formats.
        2. Write a file where data is inconsistent / not in the expected format
            for the file type.
        3. Append to an existing file.
        4. Use an invalid output path.

    Returns:
        (bool): True if successful. False otherwise.
    """
    general = GeneralIO()
    assert general.write_to_file(TEST_DIR_PATH + "/json_test.json",
                                 general.read_file(VALID_SAMPLE_JSON_FILE)[1], True) and \
        general.delete(TEST_DIR_PATH + "/json_test.json") and \
        general.write_to_file(TEST_DIR_PATH + "/yaml_test.yaml",
                              general.read_file(VALID_SAMPLE_YAML_FILE)[1], True) and \
        general.delete(TEST_DIR_PATH + "/yaml_test.yaml") and \
        general.write_to_file(TEST_DIR_PATH + "/test_test.txt",
                              general.read_file(VALID_SAMPLE_TXT_FILE)[1], True) and \
        general.delete(TEST_DIR_PATH + "/test_test.txt") and \
        general.write_to_file(TEST_DIR_PATH + "/test_test.txt",
                              general.read_file(VALID_SAMPLE_TXT_FILE)[1], False) and \
        general.delete(TEST_DIR_PATH + "/test_test.txt") and \
        not general.write_to_file(TEST_DIR_PATH + "/Test/json_test.json",
                                  general.read_file(VALID_SAMPLE_JSON_FILE)[1], True) and \
        general.write_to_file(TEST_DIR_PATH + "/test_test.apple",
                              general.read_file(VALID_SAMPLE_TXT_FILE)[1], False) and \
        general.delete(TEST_DIR_PATH + "/test_test.apple")


def test_general_io_create_directory() -> None:
    """
    Tests the create_directory method in GeneralIO

    Tests:
        1. Use a valid path.
        2. Use an invalid path.

    Returns:
        (bool): True if successful. False otherwise.
    """
    general = GeneralIO()
    assert general.create_directory(TEST_DIR_PATH + "/test") and \
        not general.create_directory(WAV_FILE_1_PATH) and \
        general.delete(TEST_DIR_PATH + "/test")


def test_general_io_move_file() -> None:
    """
    Tests the move_file method in GeneralIO

    Tests:
        1. Use a file as source / directory destination.
        2. Use a directory as source / directory destination.
        3. Use a file as destination.
        4. Use an input file / directory that does not exist.

    Returns:
        (bool): True if successful. False otherwise.
    """
    general = GeneralIO()
    # Copy some files to the test directory
    general.copy(WAV_FILE_1_PATH, TEST_DIR_PATH)
    # Get the names of all files in that directory and move them
    _, names = general.path_of_files_in_directory(
        TEST_DIR_PATH, ["wav"], False)
    name = names[0]
    # Move all the files in the test directory.
    general.move_file(name, DESKTOP_OUT_PATH)
    assert general.delete("{}/{}".format(DESKTOP_OUT_PATH,
                                         name[name.rfind("/")+1:]))


def test_general_io_copy() -> None:
    """
    Tests the copy method in GeneralIO

    Tests:
        1. Use a file as source / directory destination.
        2. Use a directory as source / directory destination.
        3. Use a file as destination.
        4. Use an input file / directory that does not exist.
        5. Use directory format for a file and vice versa.

    Returns:
        (bool): True if successful. False otherwise.
    """
    general = GeneralIO()
    assert general.copy(WAV_FILE_1_PATH, TEST_DIR_PATH) and \
        general.copy(MEDIA_TEST_DIR_PATH, TEST_DIR_PATH + "/copied") and \
        not general.copy(MEDIA_TEST_DIR_PATH, WAV_FILE_1_PATH) and \
        not general.copy(TEST_DIR_PATH + "invalid",
                         TEST_DIR_PATH + "/copied-2") and \
        general.delete(TEST_DIR_PATH + "/copied") and \
        general.delete(TEST_DIR_PATH + "/" +
                       WAV_FILE_1_PATH[WAV_FILE_1_PATH.rfind("/")+1:])


def test_general_io_rename() -> None:
    """
    Tests the rename method in GeneralIO

    Tests:
        1. Rename a file.
        2. Rename a directory.

    Returns:
        (bool): True if successful. False otherwise.
    """
    general = GeneralIO()
    file_name = WAV_FILE_1_PATH[WAV_FILE_1_PATH.rfind("/")+1:]
    assert general.copy(WAV_FILE_1_PATH, TEST_DIR_PATH)
    assert general.rename(TEST_DIR_PATH + "/" + file_name, "renamed_file")
    assert general.delete(TEST_DIR_PATH + "/renamed_file.wav")
    assert general.rename(MEDIA_TEST_DIR_PATH, "Media")
    assert general.rename(TEST_DIR_PATH + "/Media", "media")


def test_general_io_delete() -> None:
    """
    Tests the delete method in GeneralIO

    Tests:
        1. Delete a file
        2. Delete a directory with sub-directories
        3. Delete an invalid path.
        4. Use the wrong format for the file / directory.

    Returns:
        (bool): True if successful. False otherwise.
    """
    general = GeneralIO()
    # Copy some files to the test director
    general.copy(WAV_FILE_1_PATH, TEST_DIR_PATH)
    # Create a directory
    general.create_directory(TEST_DIR_PATH+"/sub")
    # Delete
    _, names = general.path_of_files_in_directory(
        TEST_DIR_PATH, ["wav"], False)
    assert all([general.delete(name,) for name in names]) and \
        general.delete(TEST_DIR_PATH+"/sub")


def test_general_io_get_parent_directory() -> None:
    """
    Tests:
        1. Get parent path of a file.
        2. Get parent path of a directory
    """
    general = GeneralIO()
    assert general.is_directory(general.get_parent_directory(WAV_FILE_1_PATH))
    assert general.is_directory(
        general.get_parent_directory(MEDIA_TEST_DIR_PATH))
