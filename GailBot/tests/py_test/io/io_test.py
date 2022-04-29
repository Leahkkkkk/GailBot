# Standard library imports
import os
import time
# Local imports
from Src.components.io import IO
from Tests.io.vardefs import *


############################### GLOBALS #####################################

########################## TEST DEFINITIONS ##################################


def test_io_is_directory() -> None:
    """
    Tests IO class is_directory function.

    Tests
        1. Confirms function returns true when given a path to a directory

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    assert io.is_directory(TEST_DIR_PATH)


def test_io_is_not_directory() -> None:
    """
    Tests IO class is_directory function.

    Tests
        1. Confirms function returns false when given a path to a file

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    assert not io.is_directory(VALID_SAMPLE_JSON_FILE)


def test_io_is_file() -> None:
    """
    Tests IO class is_file function.

    Tests:
        1. Confirms function returns true when given a path to a file.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    assert io.is_file(VALID_SAMPLE_TXT_FILE)


def test_io_is_supported_audio_file() -> None:
    """
    Tests:
        1. Check a valid audio file.
        2. Check an invalid path.
        3. Check a non-path
    """
    io = IO()
    assert io.is_supported_audio_file(WAV_FILE_1_PATH)
    assert not io.is_supported_audio_file(VIDEO_FILE_AVI_PATH)
    assert not io.is_supported_audio_file("random")


def test_io_is_supported_video_file() -> None:
    """
    Tests:
        1. Check a valid audio file.
        2. Check an invalid path.
        3. Check a non-path
    """
    io = IO()
    assert io.is_supported_video_file(VIDEO_FILE_AVI_PATH)
    assert not io.is_supported_video_file(WAV_FILE_1_COPY_PATH)
    assert not io.is_supported_video_file("random")


def test_io_is_not_file() -> None:
    """
    Tests IO class is_file function

    Tests:
        1. Confirms function returns false when given a path to a directory

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    assert not io.is_file(TEST_DIR_PATH)


def test_io_num_files_in_empty_dir() -> None:
    """
    Tests IO class number_of_files_in_directory function.

    Tests:
        1. Confirms function returns sucess with 0 files in directory.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    success, num = io.number_of_files_in_directory(
        TEST_EMPTY_DIR_PATH, ["pdf"], False)
    assert success and num == 0


def test_io_num_files_in_populated_dir() -> None:
    """
    Tests IO class number_of_files_in_directory function.

    Tests:
        1. Confirms that io returns correct number of files when type of file
           is specified.
        2. Confirms that io return correct number of files when two types of
           files are specified to be counted.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    success_pdf, num_pdf = io.number_of_files_in_directory(
        TEST_SAMPLE_DIR_PATH, ["pdf"], False)
    sucess_jpg, num_jpg = io.number_of_files_in_directory(
        TEST_SAMPLE_DIR_PATH, ["jpg"], False)
    success_pdf_jpg, num_pdf_jpg = io.number_of_files_in_directory(
        TEST_SAMPLE_DIR_PATH, ["jpg", "pdf"], False)
    assert success_pdf and sucess_jpg and success_pdf_jpg


def test_io_num_files_in_dir_wildcard() -> None:
    """
    Tests IO class number_of_files_in_directory function, wildcard type.

    Tests:
        1. Confirms that io returns correct number of files in an empty directory
           when wildcard type is specified.
        2. Confirms that io returns correct number of files in a populated
           directory when wildcard type is specified.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    success1, num1 = io.number_of_files_in_directory(
        TEST_EMPTY_DIR_PATH, ["*"], False)
    success2, num2 = io.number_of_files_in_directory(
        TEST_SAMPLE_DIR_PATH, ["*"], False)
    assert success1 and success2


def test_io_num_files_in_dir_recursive() -> None:
    """
    Tests IO class num_files_in_directory function, recursive option.

    Tests:
        1. Tests non-recursive feature in nested directory with pdfs.
        2. Tests recursive feature in nested directory with pdfs.
        3. Tests non-recursive feature in nested directory with pdfs and jpgs.
        4. Tests recursive feature in nested directory with pdfs and jpgs.
        5. Tests non-recursive feature in nested directory with wildcard.
        6. Tests recursive feature in nested directory with wildcard.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    success1, num_pdf_inner = io.number_of_files_in_directory(
        TESTS_OUTER_DIR_PATH, ["pdf"], False)
    success2, num_pdf_rec = io.number_of_files_in_directory(
        TESTS_OUTER_DIR_PATH, ["pdf"], True)
    success3, num_jpg_pdf_inner = io.number_of_files_in_directory(
        TESTS_OUTER_DIR_PATH, ["pdf", "jpg"], False)
    success4, num_jpg_pdf_rec = io.number_of_files_in_directory(
        TESTS_OUTER_DIR_PATH, ["pdf", "jpg"], True)
    success5, num_star_inner = io.number_of_files_in_directory(
        TESTS_OUTER_DIR_PATH, ["*"], False)
    success6, num_star_rec = io.number_of_files_in_directory(
        TESTS_OUTER_DIR_PATH, ["*"], True)
    assert success1 and success2 and success3 and success4 and success5 and \
        success6 and num_pdf_inner >= 0 and num_pdf_rec >= 0 and \
        num_jpg_pdf_inner >= 0 and num_jpg_pdf_rec >= 0 and \
        num_star_inner >= 0 and num_star_rec >= 0


def test_io_num_files_in_dir_bad_input() -> None:
    """
    Tests IO class number of files function with unusual input.

    Tests:
        1. Confirms that function returns (False, None) when path is not to
           a directory
        2. Confirms that function does not fail when a non-typicaly extension
           is given in options.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    success1, num1 = io.number_of_files_in_directory(KITTEN_JPG, ["*"], False)
    success2, num2 = io.number_of_files_in_directory(
        TEST_DIR_PATH, ["weird_extension"], False)
    assert not success1 and num1 == None and success2 and num2 == 0


def test_io_names_of_files_in_empty_directory() -> None:
    """
    Tests IO class path_of_files_in_directory function on empty directory.

    Tests:
        1. Confirms the function returns true and the array of files is empty
           when given a path to an empty dir.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    success, names = io.path_of_files_in_directory(
        TEST_DIR_PATH, ["pdf"], False)
    assert success and names == []


def test_io_names_of_files_in_populated_dir() -> None:
    """
    Tests IO class path_of_files_in_directory function on populated dir.

    Tests:
        1. Confirms the function return true and the array of pdf files in dir
           is correct.
        2. Confirms the function returns true and the array of pdf files in dir
           is correct with recursive option.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    success1, names1 = io.path_of_files_in_directory(
        TEST_SAMPLE_DIR_PATH, ["pdf"], False)
    success2, names2 = io.path_of_files_in_directory(
        TESTS_OUTER_DIR_PATH, ["pdf"], True)
    assert success1 and len(names1) == 0 and \
        success2 and len(names2) > 0


def test_io_number_of_subdirectories() -> None:
    """
    Tests:
        1. Provide a valid directory.
        2. Provide a file path.
        3. Provide an invalid path.
    """
    io = IO()
    assert io.number_of_subdirectories(TEST_DIR_PATH)[1] > 0
    assert not io.number_of_subdirectories(WAV_FILE_1_COPY_PATH)[0]
    assert not io.number_of_subdirectories("invalid")[0]


def test_io_paths_of_subdirectories() -> None:
    """
    Tests:
        1. Provide a valid directory.
        2. Provide a file path.
        3. Provide an invalid path.
    """
    io = IO()
    assert all([io.is_directory(path) for path
                in io.paths_of_subdirectories(TEST_DIR_PATH)[1]])
    assert not io.paths_of_subdirectories(WAV_FILE_1_COPY_PATH)[0]
    assert not io.paths_of_subdirectories("invalid")[0]


def test_io_names_of_files_wildcard() -> None:
    """
    Tests IO class names_of_files_in_directory, recursive option.

    Tests:
        1. Confirms correct names and success of wildcard option non-recursive.
        2. Confirms correct names and success of wildcard option recursive.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    success1, names1 = io.path_of_files_in_directory(
        TEST_SAMPLE_DIR_PATH, ["*"], False)
    success2, names2 = io.path_of_files_in_directory(
        TESTS_OUTER_DIR_PATH, ["*"], True)
    assert success1 and \
        success2 and len(names2) > 0


def test_io_names_of_files_bad_input() -> None:
    """
    Tests IO class name of files function with unusual input.

    Tests:
        1. Confirms that function returns (False, None) when path is not to
           a directory
        2. Confirms that function does not fail when a non-typical extension
           is given in options.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    success1, names1 = io.path_of_files_in_directory(KITTEN_JPG, ["*"], False)
    success2, names2 = io.path_of_files_in_directory(
        TEST_DIR_PATH, ["weird_extension"], False)
    assert not success1 and names1 == [] and success2 and names2 == []


def test_io_get_supported_audio_formats() -> None:
    """
    Tests:
        1. Check the correct formats are returned.
    """
    io = IO()
    assert io.get_supported_audio_formats() == ("mp3", "mpeg", "opus", "wav")


def test_io_get_supported_video_formats() -> None:
    """
    Tests:
        1. Check the correct formats are returned.
    """
    io = IO()
    assert len(io.get_supported_video_formats()) > 0


def test_io_read_valid_json() -> None:
    """
    Tests IO class read of json file.

    Tests:
        1. Reads valid json file.
        2. Confirms sucessful read and checks correct data.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    success, data = io.read(VALID_SAMPLE_JSON_FILE)
    assert success and data == {"Test_key": "I am a test string"}


def test_io_read_valid_yaml() -> None:
    """
    Tests IO class read of yaml file.

    Tests:
        1. Read valid yaml file.
        2. Confirms successful read and checks correct data.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    success, data = io.read(VALID_FRUITS_YAML_FILE)
    assert success and data == {'blueberries': 100}


def test_io_read_valid_text() -> None:
    """
    Tests IO class read of text file.

    Tests:
        1. Read valid text file.
        2. Confirms sucessful read and checks correct data.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    success, data = io.read(VALID_SMALL_TXT_FILE)
    assert success and data == "This is a test text file"


def test_io_read_invalid() -> None:
    """
    Tests IO class read of non-readable files.

    Tests:
        1. Confirms unsuccessful read of jpg.
        2. Confirms unsuccessful read of pdf.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    success1, data1 = io.read(GOAT_JPG)
    success2, data2 = io.read(BEE_MOVIE)
    assert not success1 and data1 == None and not success2 and data2 == None


def test_io_write_existing_json() -> None:
    """
    Tests IO class write of already existing file without overwrite.

    Tests:
        1. Writes to existing file with false overwrite.
        2. Confirms unsucessful write.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    success1 = io.write(VALID_SAMPLE_JSON_FILE, {"hello : key"}, False)
    assert not success1


def test_io_is_not_file() -> None:
    """
    Tests IO class is_file function.

    Tests:
        1. Confirms function returns false when given a path to a directory.

    Tests:
        1. Converts yaml to json.
        2. Reads data from yaml and json.
        3. Deletes converted file.
        4. Confirms success and compares data.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    success = io.convert_format(
        VALID_SAMPLE_YAML_FILE, "JSON", TEST_EMPTY_DIR_PATH)
    _, yaml_data = io.read(VALID_SAMPLE_YAML_FILE)
    _, json_data = io.read(TEST_EMPTY_DIR_PATH + "/sample_yaml.JSON")
    io.delete(TEST_EMPTY_DIR_PATH + "/sample_yaml.JSON")
    assert success and yaml_data == json_data


def test_io_convert_txt_to_yaml() -> None:
    """
    Tests io_convert with text and yaml file.

    Tests:
        1. Attempts to convert text file not in dictionary form to yaml file.
        2. Confirms conversion was unsucessful.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    success = io.convert_format(
        VALID_SAMPLE_TXT_FILE, "yaml", TEST_EMPTY_DIR_PATH)
    assert not success


def test_io_create_directory() -> None:
    """
    Tests IO class create_directory function.

    Tests:
        1. Creates directory in empty directory.
        2. Checks that new directory exists.
        3. Deletes new directory.
        4. Confirms results.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    success = io.create_directory(TEST_EMPTY_DIR_PATH + "/test_dir")
    is_dir = io.is_directory(TEST_EMPTY_DIR_PATH + "/test_dir")
    io.delete(TEST_EMPTY_DIR_PATH + "/test_dir")
    assert success and is_dir


def test_io_create_invalid_directory() -> None:
    """
    Tests IO class create_directory in invalid path case.

    Tests:
        1. Attempts to create directory to a path that is not a dir.
        2. Confirms unsucessful create.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    success = io.create_directory(BDAY_CAT_JPG + "/test_dir/more")
    assert not success


def test_io_move_file() -> None:
    """
    Tests IO class move function.

    Tests:
        1. Moves file to empty dir
        2. Checks that file can be found in new dest
        3. Checks that original file cannot be found at source
        4. Moves file back to original src
        5. Confirms above results

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    assert io.is_file(KITTEN_JPG)
    assert io.move_file(KITTEN_JPG, TEST_EMPTY_DIR_PATH)
    assert io.is_file(TEST_EMPTY_DIR_PATH + "/kitten_tongue.jpg")
    assert not io.is_file(KITTEN_JPG)
    assert io.move_file(TEST_EMPTY_DIR_PATH + "/kitten_tongue.jpg",
                        KITTEN_JPG[:KITTEN_JPG.rfind('/')])


def test_io_copy() -> None:
    """
    Tests IO class copy function.

    Tests:
        1. Copies jpg to empty dir.
        2. Checks that the copy exists.
        3. Check that the original copy still exists.
        4. Deletes new copy.
        5. Confirms results.

     Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    assert io.is_file(KITTEN_JPG)
    assert io.copy(KITTEN_JPG, TEST_EMPTY_DIR_PATH)
    assert io.is_file(TEST_EMPTY_DIR_PATH + "/kitten_tongue.jpg")
    assert io.is_file(KITTEN_JPG)
    assert io.delete(TEST_EMPTY_DIR_PATH + "/kitten_tongue.jpg")


def test_io_rename() -> None:
    """
    Tests IO class rename function.

    Tests:
        1. Renames jpg.
        2. Checks that renamed file can be found.
        3. Rename jpg to original name.
        4. Confirms results.

     Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    assert io.rename(KITTEN_JPG, "kitten")
    assert io.is_file(KITTEN_JPG[:KITTEN_JPG.rfind('/')] + "/kitten.jpg")
    assert io.rename(KITTEN_JPG[:KITTEN_JPG.rfind(
        '/')] + "/kitten.jpg", "kitten_tongue")


def test_io_record_audio() -> None:
    """
    Test the record_audio method in IO.

    Tests:
        1. Test with valid paramters.
        2. Check with negative recording duration.
        3. Check with invalid output path.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    assert io.record_audio(10, "recording", TEST_EMPTY_DIR_PATH)[0] and \
        not io.record_audio(-10, "recording", TEST_EMPTY_DIR_PATH)[0] and \
        not io.record_audio(10, "recording", VALID_SAMPLE_JSON_FILE)[0] and \
        io.delete(TEST_EMPTY_DIR_PATH + "/recording.wav")


def test_io_mono_to_stereo() -> None:
    """
    Test the mono_to_stereo method in IO.

    Tests:
        1. Pass valid files
        2. Pass files with different numbers of frames.
        2. Pass invalid files i.e. directories

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    s1, name = io.mono_to_stereo(
        WAV_FILE_1_PATH, WAV_FILE_1_COPY_PATH, TEST_EMPTY_DIR_PATH)
    assert s1 and \
        not io.mono_to_stereo(WAV_FILE_1_PATH, WAV_FILE_2_PATH, TEST_EMPTY_DIR_PATH)[0] and \
        not io.mono_to_stereo(TEST_EMPTY_DIR_PATH, WAV_FILE_1_COPY_PATH, TEST_EMPTY_DIR_PATH)[0] and \
        io.delete("{}/{}.{}".format(TEST_EMPTY_DIR_PATH, name, "wav"))


def test_io_mono_stereo_valid() -> None:
    """
    Test the mono_to_stereo method in IO with valid file.

    Tests:
        1. Pass valid files to io.mono_to_stereo.
        2. Check that sucess was returned, file exists and deleted.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    s1, name = io.mono_to_stereo(
        WAV_FILE_1_PATH, WAV_FILE_1_COPY_PATH, TEST_EMPTY_DIR_PATH)
    is_file = io.is_file("{}/{}.{}".format(TEST_EMPTY_DIR_PATH, name, "wav"))
    deleted = io.delete("{}/{}.{}".format(TEST_EMPTY_DIR_PATH, name, "wav"))
    assert s1 and is_file and deleted

# TODO: mismatch in returns here


def test_io_mono_stereo_invalid_frames() -> None:
    """
    Tests the mono_to_stereo method in IO with files with mismatched frames.

    Tests:
        1. Pass two files with different numbers of frames.
        2. Confirm the return in unsucessful.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    s1, name = io.mono_to_stereo(
        WAV_FILE_1_PATH, WAV_FILE_2_PATH, TEST_EMPTY_DIR_PATH)
    assert not s1 and name == None


def test_io_mono_stereo_invalid_files() -> None:
    """
    Tests the mono_to_stereo method in IO with directories.

    Tests:
        1. Pass two directories into mono_to_stereo.
        2. Confirm the return is unsucessful.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    s1, name = io.mono_to_stereo(
        TEST_EMPTY_DIR_PATH, WAV_FILE_1_COPY_PATH, TEST_EMPTY_DIR_PATH)
    #assert io.is_file("{}/{}.{}".format(TEST_EMPTY_DIR_PATH,name,"wav"))
    assert not s1
    #assert not s1 and name == None


def test_io_stereo_to_mono() -> None:
    """
    Tests the stereo_to_mono method in IO.

    Tests:
        1. Provide a valid stereo file.
        2. Provide a mono file.
        3. Provide a directory.
        4. Provide invalid output directory path.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    s1, identifiers = io.stereo_to_mono(
        STEREO_FILE_1_PATH, TEST_EMPTY_DIR_PATH)
    s2, _ = io.stereo_to_mono(WAV_FILE_1_COPY_PATH, TEST_EMPTY_DIR_PATH)
    s3, _ = io.stereo_to_mono(TEST_EMPTY_DIR_PATH, TEST_EMPTY_DIR_PATH)
    s4, _ = io.stereo_to_mono(WAV_FILE_1_PATH, WAV_FILE_1_PATH)
    assert s1 and not s2 and not s3 and not s4 and \
        io.delete("{}/{}.{}".format(TEST_EMPTY_DIR_PATH, identifiers[0], "wav")) and \
        io.delete("{}/{}.{}".format(TEST_EMPTY_DIR_PATH,
                  identifiers[1], "wav"))


def test_io_stereo_mono_valid() -> None:
    """
    Tests the stereo_to_mono method in IO with valid data.

    Tests:
        1. Passes valid stereo file to function.
        2. Confirms that call was unsucessful.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    s1, identifiers = io.stereo_to_mono(
        STEREO_FILE_1_PATH, TEST_EMPTY_DIR_PATH)
    is_file1 = io.is_file(
        "{}/{}.{}".format(TEST_EMPTY_DIR_PATH, identifiers[0], "wav"))
    is_file2 = io.is_file(
        "{}/{}.{}".format(TEST_EMPTY_DIR_PATH, identifiers[1], "wav"))
    deleted1 = io.delete(
        "{}/{}.{}".format(TEST_EMPTY_DIR_PATH, identifiers[0], "wav"))
    deleted2 = io.delete(
        "{}/{}.{}".format(TEST_EMPTY_DIR_PATH, identifiers[1], "wav"))
    assert s1 and is_file1 and is_file2 and deleted1 and deleted2

# TODO: (None, None)?


def test_io_stereo_mono_invalid_mono() -> None:
    """
    Tests the stereo_to_mono method in IO with a mono file.

    Tests:
        1. Passes a mono file for conversion.
        2. Confirms that call was unsuccessful.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    s1, names = io.stereo_to_mono(WAV_FILE_1_COPY_PATH, TEST_EMPTY_DIR_PATH)
    assert not s1 and names == (None, None)


def test_io_stereo_mono_invalid_file() -> None:
    """
    Tests the stereo_to_mono method in io with a directory.

    Test:
        1. Passes a directory for conversion.
        2. Confirms that call was unsuccessful.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    s1, names = io.stereo_to_mono(TEST_EMPTY_DIR_PATH, TEST_EMPTY_DIR_PATH)
    assert not s1 and names == (None, None)

# TODO: (None, None)?


def test_io_stereo_mono_invalid_output_path() -> None:
    """
    Tests the stereo_to_mono method in io with an invalid output path.

    Tests
        1. Provides invalid output path to function.
        2. Confirms that conversion was unsuccesful.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    s1, names = io.stereo_to_mono(WAV_FILE_1_PATH, WAV_FILE_1_PATH)
    assert not s1 and names == (None, None)


def test_io_concat() -> None:
    """
    Tests the concat method in IO.

    Tests:
        1. Concat files with the same extension.
        2. Concat files with different extensions.
        3. Concat non-files i.e., directories.
        4. Provide invalid output directory path.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    s1, identifier = io.concat(
        [WAV_FILE_1_PATH, WAV_FILE_2_PATH, WAV_FILE_3_PATH], TEST_EMPTY_DIR_PATH)
    s2, _ = io.concat([WAV_FILE_1_PATH, VIDEO_FILE_MP4_PATH],
                      TEST_EMPTY_DIR_PATH)
    s3, _ = io.concat(
        [TEST_EMPTY_DIR_PATH, TEST_EMPTY_DIR_PATH], TEST_EMPTY_DIR_PATH)
    s4, _ = io.concat([WAV_FILE_1_PATH, WAV_FILE_2_PATH,
                      WAV_FILE_3_PATH], WAV_FILE_1_COPY_PATH)
    assert s1 and not s2 and not s3 and not s4 and \
        io.delete("{}/{}.{}".format(TEST_EMPTY_DIR_PATH, identifier, "wav"))


def test_io_concat_valid() -> None:
    """
    Tests the concat method in IO with valid files.

    Tests:
        1. Concat audio files with same extension.
        2. Confirm concat was successful.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    s1, identifier = io.concat(
        [WAV_FILE_1_PATH, WAV_FILE_2_PATH, WAV_FILE_3_PATH], TEST_EMPTY_DIR_PATH)
    is_file = io.is_file(
        "{}/{}.{}".format(TEST_EMPTY_DIR_PATH, identifier, "wav"))
    deleted = io.delete(
        "{}/{}.{}".format(TEST_EMPTY_DIR_PATH, identifier, "wav"))
    assert s1 and is_file and deleted


def test_io_concat_invalid_extensions() -> None:
    """
    Tests the concat method in IO with invalid extensions.

    Tests:
        1. Concat audio files with different extensions.
        2. Confirm concat was unsuccessful.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    s1, name = io.concat(
        [WAV_FILE_1_PATH, VIDEO_FILE_MP4_PATH], TEST_EMPTY_DIR_PATH)
    assert not s1 and name == None


def test_io_concat_invalid_files() -> None:
    """
    Tests the concat method with invalid non-audio files (directories).

    Tests:
        1. Passes directories to concat.
        2. Confirms concat was unsucessful.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    s1, name = io.concat(
        [TEST_EMPTY_DIR_PATH, TEST_EMPTY_DIR_PATH], TEST_EMPTY_DIR_PATH)
    assert not s1 and name == None

# TODO: return not none here -- test2a_test2b_test_concatenated


def test_io_concat_invalid_output() -> None:
    """
    Tests the concat method with a bad output directory path.

    Tests:
        1. Passes a file as output directory.
        2. Confirms concat was unsucessful.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    s1, name = io.concat([WAV_FILE_1_PATH, WAV_FILE_2_PATH,
                         WAV_FILE_3_PATH], WAV_FILE_1_COPY_PATH)
    assert not s1 and name == None


def test_io_overlay() -> None:
    """
    Test the overlay method in IO.

    Tests:
        1. Overlay two valid files.
        2. Overlay a valid audio file with an invalid video file.
        3. Overlay a number of files not equal to 2.
        4 Provide invalid output directory.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    s1, identifier = io.overlay(
        [WAV_FILE_1_PATH, WAV_FILE_2_PATH], TEST_EMPTY_DIR_PATH)
    s2, _ = io.overlay(
        [WAV_FILE_1_PATH, VIDEO_FILE_MP4_PATH], TEST_EMPTY_DIR_PATH)
    s3, _ = io.overlay([WAV_FILE_1_PATH, WAV_FILE_2_PATH,
                       WAV_FILE_3_PATH], TEST_EMPTY_DIR_PATH)
    s4, _ = io.overlay([WAV_FILE_1_PATH, WAV_FILE_2_PATH], WAV_FILE_1_PATH)
    assert s1 and not s2 and not s3 and not s4 and \
        io.delete("{}/{}.{}".format(TEST_EMPTY_DIR_PATH, identifier, "wav"))


def test_io_overlay_valid() -> None:
    """
    Tests the overlay method in IO with valid files.

    Tests:
        1. Overlay two valid files.
        2. Confirm overlay was sucessful.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    s1, identifier = io.overlay(
        [WAV_FILE_1_PATH, WAV_FILE_2_PATH], TEST_EMPTY_DIR_PATH)
    is_file = io.is_file(
        "{}/{}.{}".format(TEST_EMPTY_DIR_PATH, identifier, "wav"))
    deleted = io.delete(
        "{}/{}.{}".format(TEST_EMPTY_DIR_PATH, identifier, "wav"))
    assert s1 and is_file and deleted


def test_io_overlay_invalid_video() -> None:
    """
    Tests the overlay method in IO with an invalid video file.

    Tests:
        1. Attempt to overlay with a video file.
        2. Confirm overlay was unsucessful.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    s1, name = io.overlay(
        [WAV_FILE_1_PATH, VIDEO_FILE_MP4_PATH], TEST_EMPTY_DIR_PATH)
    assert not s1 and name == None


def test_io_overlay_invalid_num_files() -> None:
    """
    Tests the overlay method in IO with an invalid number of files.

    Tests:
        1. Attempts to overlay three files.
        2. Confirm that overlay was unsuccesful.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    s1, name = io.overlay(
        [WAV_FILE_1_PATH, WAV_FILE_2_PATH, WAV_FILE_3_PATH], TEST_EMPTY_DIR_PATH)
    assert not s1 and name == None

# TODO: name is not None, test2a_test2b_overlaid


def test_io_overlay_invalid_output_dir() -> None:
    """
    Tests the overlay method in IO with an invalid output path.

    Tests:
        1. Passes file path to output path.
        2. Confirm that overlay was unsuccesful.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    s1, name = io.overlay([WAV_FILE_1_PATH, WAV_FILE_2_PATH], WAV_FILE_1_PATH)
    assert not s1

# TODO: documentation is wrong for test


def test_io_change_volume() -> None:
    """
    Tests the change_volume method in IO.

    Tests:
        1. Change volume to a valid number.
        2. Change to an invalid number.
        3. Provide invalid input file.
        4. Provide invalid output directory.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    name = WAV_FILE_1_PATH[WAV_FILE_1_PATH.rfind("/")+1:]
    s1 = io.change_volume(WAV_FILE_1_PATH, 20, TEST_EMPTY_DIR_PATH)
    s2 = io.change_volume(WAV_FILE_1_PATH, -20, TEST_EMPTY_DIR_PATH)
    s3 = io.change_volume(VIDEO_FILE_MP4_PATH, 100, TEST_EMPTY_DIR_PATH)
    s4 = io.change_volume(WAV_FILE_1_PATH, 20, WAV_FILE_1_PATH)
    assert s1 and s2 and not s3 and not s4 and \
        io.delete("{}/{}".format(TEST_EMPTY_DIR_PATH, name))


def test_io_reverse_audio() -> None:
    """
    Test the reverse audio method in IO.

    Tests:
        1. Reverse a valid audio file.
        2. Provide an invalid input file.
        3. Provide an invalid output directory.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    name = WAV_FILE_1_PATH[WAV_FILE_1_PATH.rfind("/")+1:]
    s1 = io.reverse_audio(WAV_FILE_1_PATH, TEST_EMPTY_DIR_PATH)
    s2 = io.reverse_audio(VIDEO_FILE_MP4_PATH, TEST_EMPTY_DIR_PATH)
    s3 = io.reverse_audio(WAV_FILE_2_PATH, WAV_FILE_2_PATH)
    assert s1 and not s2 and not s3 and \
        io.delete("{}/{}".format(TEST_EMPTY_DIR_PATH, name))


def test_io_reverse_valid() -> None:
    """
    Tests reverse method in IO with valid files.

    Tests:
        1. Reverses a valid audio file.
        2. Confirms reverse was succesful.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    name = WAV_FILE_1_PATH[WAV_FILE_1_PATH.rfind("/")+1:]
    s1 = io.reverse_audio(WAV_FILE_1_PATH, TEST_EMPTY_DIR_PATH)
    is_file = io.is_file("{}/{}".format(TEST_EMPTY_DIR_PATH, name))
    deleted = io.delete("{}/{}".format(TEST_EMPTY_DIR_PATH, name))
    assert s1 and is_file and deleted


def test_io_reverse_invalid_input() -> None:
    """
    Tests reverse method with invalid input files.

    Tests:
        1. Attempts to reverse video file.
        2. Confirms that reverse was unsuccessful.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    s1 = io.reverse_audio(VIDEO_FILE_MP4_PATH, TEST_EMPTY_DIR_PATH)
    is_empty = io.number_of_files_in_directory(
        TEST_EMPTY_DIR_PATH, ["*"], True)[1] == 0
    assert not s1 and is_empty


def test_io_reverse_invalid_output() -> None:
    """
    Tests reverse method with invalid output path.

    Tests:
        1. Passes file as output path.
        2. Confirms that rever was unsuccessful.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    s1 = io.reverse_audio(WAV_FILE_2_PATH, WAV_FILE_2_PATH)
    is_empty = io.number_of_files_in_directory(
        TEST_EMPTY_DIR_PATH, ["*"], True)[1] == 0
    assert not s1 and is_empty


def test_io_chunk() -> None:
    """
    Tests the chunk method in IO.

    Tests:
        1. Chunk a valid audio file.
        2. Chunk an invalid file.
        3. Chunk with a negative chunk duration.
        4. Use an invalid outout directory.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    # Create a directory to store chunks.
    dir_path = TEST_EMPTY_DIR_PATH + "/chunks"
    io.create_directory(dir_path)
    s1 = io.chunk(WAV_FILE_1_PATH, dir_path, 10)
    s2 = io.chunk(VIDEO_FILE_MP4_PATH, dir_path, 10)
    s3 = io.chunk(WAV_FILE_1_PATH, dir_path, -10)
    s4 = io.chunk(WAV_FILE_1_PATH, WAV_FILE_1_COPY_PATH, 10)
    assert s1 and not s2 and not s3 and not s4 and \
        io.delete(dir_path)


def test_io_extract_video_from_file() -> None:
    """
    Tests the extract_video_from_file method in IO.

    Tests:
        1. Extract video from a valid video file.
        2. Extract from an invalid file
        3. Provide an invalid output directory path.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    name = "sample-mov-file.mp4"
    assert io.extract_video_from_file(VIDEO_FILE_MOV_PATH, TEST_EMPTY_DIR_PATH) and \
        io.is_file("{}/{}".format(TEST_EMPTY_DIR_PATH, name)) and \
        io.delete("{}/{}".format(TEST_EMPTY_DIR_PATH, name)) and \
        not io.extract_video_from_file(WAV_FILE_1_COPY_PATH, TEST_EMPTY_DIR_PATH) and \
        not io.extract_video_from_file(VIDEO_FILE_MOV_PATH, WAV_FILE_1_PATH)


def test_io_extract_video_from_file_not_movie() -> None:
    """
    Tests extract_video_from_file method in IO with a non-movie file.

    Tests:
        1. Attempts to extract video from an audio file.
        2. Confirms the extraction was unsuccesful.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    s1 = io.extract_video_from_file(WAV_FILE_1_PATH, TEST_EMPTY_DIR_PATH)
    assert not s1


def test_io_extract_video_from_file_bad_dir() -> None:
    """
    Tests extract_video_from_file method in IO with a bad output directory

    Tests:
        1. Passes file path to output directory path
        2.  Confrims the extraction was unsuccesful.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    s1 = io.extract_video_from_file(VIDEO_FILE_MOV_PATH, KITTEN_JPG)
    assert not s1


def test_io_extract_audio_from_file() -> None:
    """
    Tests the extract_audio_from_file method in IO.

    Tests:
        1. Use a valid input file and directory.
        2. Use an invalid input file.
        3. Provide an invalid output directory path.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    assert io.extract_audio_from_file(VIDEO_FILE_MOV_PATH, TEST_EMPTY_DIR_PATH) and \
        io.is_file(TEST_EMPTY_DIR_PATH + "/sample-mov-file.wav") and \
        io.delete(TEST_EMPTY_DIR_PATH + "/sample-mov-file.wav") and \
        not io.extract_audio_from_file(WAV_FILE_1_PATH, TEST_EMPTY_DIR_PATH) and \
        not io.extract_audio_from_file(
            VIDEO_FILE_MOV_PATH, VIDEO_FILE_AVI_PATH)


def test_io_extract_audio_from_file_not_movie() -> None:
    """
    Tests the extract_audio_from_file method in IO with a non-movie file

    Tests:
        1. Attempt to extract audio from non-movie file
        2. Confirms that extraction was unsuccesful

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    s1 = io.extract_audio_from_file(WAV_FILE_1_PATH, TEST_EMPTY_DIR_PATH)
    assert not s1


def test_io_extract_audio_from_file_bad_dir() -> None:
    """
    Tests the extract_audio_from_file with a bad output path

    Tests:
        1. Passes a jpg file as the output path for function.
        2. Confirms that extraction was unsucessful.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    s1 = io.extract_audio_from_file(VIDEO_FILE_MOV_PATH, KITTEN_JPG)
    assert not s1


def test_io_run_shell_command() -> None:
    """
    Tests the run_shell_command method in IO.

    Tests:
        1. Run a valid shell command
        2. Run an invalid shell command

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    assert io.run_shell_command("pwd", None, None)[0] and \
        io.run_shell_command("invalid", None, None)[0]


def test_io_get_shell_process_status() -> None:
    """
    Tests the get_shell_process_status method in IO.

    Tests:
        1. Get status of a command that finished
        2. Get status of a command that results in an error

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    s1, identifier_valid = io.run_shell_command("pwd", None, None)
    s2, identifier_invalid = io.run_shell_command("invalid", None, None)
    time.sleep(1)
    assert s1 and s2 and \
        io.get_shell_process_status(identifier_valid) == "finished" and \
        io.get_shell_process_status(identifier_invalid) == "error"


def test_io_get_size() -> None:
    """
    Tests the get_size method in IO

    Tests:
        1. Get size of valid file.
        2. Get size of valid directory.
        3. Get size of invalid path

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    assert io.get_size(WAV_FILE_1_PATH)[0] and \
        io.get_size(TEST_DIR_PATH)[0] and \
        not io.get_size("INvalid/path")[0]


def test_io_get_name() -> None:
    """
    Tests the get_name method in IO.

    Tests:
        1. Get the name of a valid file
        2. Get the name of a valid directory.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    assert io.get_name(WAV_FILE_1_PATH) == "test2a" and \
        io.get_name(TEST_EMPTY_DIR_PATH) == "empty_dir_1"


def test_io_get_file_extension() -> None:
    """
    Tests the get_file_extension method in IO.

    Tests:
        1. Get extension of a valid file.
        2. Get extension of a directory.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    assert io.get_file_extension(WAV_FILE_1_PATH)[1] == "wav" and \
        not io.get_file_extension(TEST_EMPTY_DIR_PATH)[0]


def test_io_get_parent_path() -> None:
    """
    Tests:
        1. Obtain the parent path of a file.
        2. Obtain the parent path of a directory.
        3. Obtain parent path of a random string.
    """
    io = IO()
    assert io.is_directory(io.get_parent_path(WAV_FILE_1_PATH))
    assert io.is_directory(io.get_parent_path(TEST_DIR_PATH))
    assert io.get_parent_path("random") == ""
