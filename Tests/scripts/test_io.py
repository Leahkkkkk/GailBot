"""
Testing script for the IO component.
"""
# Standard library imports 
import os 
import time
# Local imports 

# Third party imports 
from Src.Components.io import  AudioIO, VideoIO, VideoWriteTypes,\
                         GeneralIO, ShellIO, ShellStatus, IO
from ..suites import TestSuite

############################### GLOBALS #####################################

#### Relative paths
WAV_FILE_1_PATH = "Test_files/Media/test2a.wav"
WAV_FILE_1_COPY_PATH = "Test_files/Media/test2a_copy.wav"
WAV_FILE_2_PATH = "Test_files/Media/test2b.wav"
WAV_FILE_3_PATH = "Test_files/Media/test.wav"
STEREO_FILE_1_PATH = "Test_files/Media/SineWaveMinus16.wav"
VIDEO_FILE_MP4_PATH = "Test_files/Media/sample-mp4-file.mp4"
VIDEO_FILE_MXF_PATH = "Test_files/Media/vid2.MXF"
VIDEO_FILE_AVI_PATH = "Test_files/Media/sample-avi-file.avi"
VIDEO_FILE_MOV_PATH = "Test_files/Media/sample-mov-file.mov"
VIDEO_FILE_MPG_PATH = "Test_files/Media/sample-mpg-file.mpg"
DESKTOP_OUT_PATH = os.path.join(os.path.join(os.path.expanduser('~')),'Desktop') 
VALID_SAMPLE_JSON_FILE = "Test_files/Others/sample_config.json"
VALID_SAMPLE_TXT_FILE = "Test_files/Others/sample_text.txt"
VALID_SMALL_TXT_FILE = "Test_files/Others/textfile.txt"
VALID_SAMPLE_YAML_FILE = "Test_files/Others/sample_yaml.yaml"
VALID_FRUITS_YAML_FILE = "Test_files/Others/fruits.yaml"
TEST_DIR_PATH = "Test_files"
TEST_SAMPLE_DIR_PATH = "Test_files/Others/Test-directory-2/inner_directory"
TESTS_OUTER_DIR_PATH = "Test_files/Others/Test-directory-2"
TEST_EMPTY_DIR_PATH = "Test_files/Others/Test-directory"
MEDIA_TEST_DIR_PATH = "Test_files/Media"
NORMAN_TEXT = "Test_files/Others/Test-directory-2/inner_directory/norman_text.pdf"
BEE_MOVIE = "Test_files/Others/Test-directory-2/bee_movie.pdf"
PANDA_JPG = "Test_files/Others/Test-directory-2/panda.jpg"
RACCOON_JPG = "Test_files/Others/Test-directory-2/racoon_math.jpg"
KITTEN_JPG = "Test_files/Others/Test-directory-2/inner_directory/kitten_tongue.jpg"
BDAY_CAT_JPG = "Test_files/Others/Test-directory-2/inner_directory/sad_bday_cat.jpg"
GOAT_JPG = "Test_files/Others/Test-directory-2/inner_directory/skater_goat.jpg"

########################## TEST DEFINITIONS ##################################

######################### GeneralIO tests

def test_general_io_is_directory() -> bool:
    """
    Tests the is_directory method in GeneralIO

    Tests:
        1. Use on a valid directory.
        2. Use on an invalid directory

    Returns:
        (bool): True if successful. False otherwise.
    """
    general = GeneralIO() 
    return general.is_directory(TEST_DIR_PATH) and \
        not general.is_directory(WAV_FILE_1_PATH)


def test_general_io_is_file() -> bool:
    """
    Tests the is_file method in GeneralIO

    Tests:
        1. Use on a valid file.
        2. Use on an invalid file 

    Returns:
        (bool): True if successful. False otherwise.
    """
    general = GeneralIO() 
    return not general.is_file(TEST_DIR_PATH) and \
        general.is_file(WAV_FILE_1_PATH)

def test_general_io_num_files_in_directory() -> bool:
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
    return general.number_of_files_in_directory(TEST_DIR_PATH)[1] == 0 and \
        not general.number_of_files_in_directory(WAV_FILE_1_PATH)[0] and \
        general.number_of_files_in_directory(MEDIA_TEST_DIR_PATH,["avi"])[1] == 1 and \
        general.number_of_files_in_directory(TEST_DIR_PATH,[".asjkd.j"])[1] == 0 and \
        general.number_of_files_in_directory(TEST_DIR_PATH,["avi"],True)[1] == 1

def test_general_io_path_of_files_in_directory() -> bool:
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
    return general.path_of_files_in_directory(TEST_DIR_PATH)[0] and \
        not general.path_of_files_in_directory(WAV_FILE_1_PATH)[0] and \
        general.path_of_files_in_directory(TEST_DIR_PATH,["pdf"])[0] and \
        general.number_of_files_in_directory(TEST_DIR_PATH,[".asjkd.j"])[1] == 0 and \
        general.number_of_files_in_directory(TEST_DIR_PATH,["pdf"],True)[0]

def test_general_io_is_readable() -> bool:
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
    return general.is_readable(VALID_SAMPLE_TXT_FILE) and \
        general.is_readable(VALID_SAMPLE_JSON_FILE) and \
        general.is_readable(VALID_SAMPLE_YAML_FILE) and \
        not general.is_readable(WAV_FILE_1_PATH) and \
        not general.is_readable(VIDEO_FILE_AVI_PATH) and \
        not general.is_readable(TEST_DIR_PATH) 

def test_general_io_get_file_extension() -> bool:
    """
    Tests the get file extension method in GeneralIO.

    Tests:
        1. Read a file and get extension.
        2. Try to get extension of a directory. 
    
    Returns:
        (bool): True if successful. False otherwise.
    """
    general = GeneralIO()
    return general.get_file_extension(WAV_FILE_1_PATH) == "wav" and \
        general.get_file_extension(TEST_DIR_PATH) == ""

def test_general_io_read_files() -> bool:
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
    return general.read_file(VALID_SAMPLE_JSON_FILE,)[0] and \
        general.read_file(VALID_SAMPLE_TXT_FILE)[0] and \
        general.read_file(VALID_SAMPLE_YAML_FILE,)[0] and \
        not general.read_file(VIDEO_FILE_AVI_PATH)[0] and \
        not general.read_file(TEST_DIR_PATH)[0]

def test_general_io_write_to_file() -> bool:
    """
    Tests the write_to_file method in GeneralIO

    Tests:
        1. Write a valid file in all types of supported formats.
        2. Write a file where data is inconsistent / not in the expected format 
            for the file type.
        3. Append to an existing file.
        4. Use an invalid output path.
        5. Use an invalid output file extension.

    Returns:
        (bool): True if successful. False otherwise.
    """
    general = GeneralIO() 
    return general.write_to_file(TEST_DIR_PATH + "/json_test.json",
        general.read_file(VALID_SAMPLE_JSON_FILE)[1], True) and \
        general.delete(TEST_DIR_PATH +"/json_test.json") and \
        general.write_to_file(TEST_DIR_PATH + "/yaml_test.yaml", 
        general.read_file(VALID_SAMPLE_YAML_FILE)[1], True) and \
        general.delete(TEST_DIR_PATH +"/yaml_test.yaml") and \
        general.write_to_file(TEST_DIR_PATH+ "/test_test.txt", 
        general.read_file(VALID_SAMPLE_TXT_FILE)[1], True) and \
        general.delete(TEST_DIR_PATH +"/test_test.txt") and \
        general.write_to_file(TEST_DIR_PATH +"/test_test.txt", 
        general.read_file(VALID_SAMPLE_TXT_FILE)[1], False) and \
        general.delete(TEST_DIR_PATH +"/test_test.txt") and \
        not general.write_to_file(TEST_DIR_PATH +"/Test/json_test.json",
        general.read_file(VALID_SAMPLE_JSON_FILE)[1], True) and \
        not general.write_to_file(TEST_DIR_PATH +"/test_test.apple", 
        general.read_file(VALID_SAMPLE_TXT_FILE)[1], False)

def test_general_io_create_directory() -> bool:
    """
    Tests the create_directory method in GeneralIO

    Tests:
        1. Use a valid path.
        2. Use an invalid path.

    Returns:
        (bool): True if successful. False otherwise.
    """
    general = GeneralIO()
    return general.create_directory(TEST_DIR_PATH + "/test") and \
        not general.create_directory(WAV_FILE_1_PATH) and \
        general.delete(TEST_DIR_PATH + "/test")

def test_general_io_move_file() -> bool:
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
    general.copy(WAV_FILE_1_PATH,TEST_DIR_PATH)
    # Get the names of all files in that directory and move them
    _, names = general.path_of_files_in_directory(
        TEST_DIR_PATH,["wav"],False)
    name = names[0]
    # Move all the files in the test directory.
    if not general.move_file(name,DESKTOP_OUT_PATH):
        return False 
    return general.delete("{}/{}".format(DESKTOP_OUT_PATH,
            name[name.rfind("/")+1:]))

def test_general_io_copy() -> bool:
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
    return general.copy(WAV_FILE_1_PATH, TEST_DIR_PATH) and \
        general.copy(MEDIA_TEST_DIR_PATH,TEST_DIR_PATH + "/copied") and \
        not general.copy(MEDIA_TEST_DIR_PATH , WAV_FILE_1_PATH) and \
        not general.copy(TEST_DIR_PATH + "invalid",
            TEST_DIR_PATH + "/copied-2") and \
        general.delete(TEST_DIR_PATH +"/copied") and \
        general.delete(TEST_DIR_PATH + "/" + \
            WAV_FILE_1_PATH[WAV_FILE_1_PATH.rfind("/")+1:])

def test_general_io_rename() -> bool:
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

    return general.copy(WAV_FILE_1_PATH, TEST_DIR_PATH) and \
        general.rename(TEST_DIR_PATH + "/" + file_name, "renamed_file") and \
        general.delete(TEST_DIR_PATH + "/renamed_file.wav") and \
        general.rename(MEDIA_TEST_DIR_PATH, "media") and \
        general.rename(TEST_DIR_PATH + "/media", "Media")
    

def test_general_io_delete() -> bool:
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
        TEST_DIR_PATH,["wav"],False)
    return all([general.delete(name,) for name in names]) and \
        general.delete(TEST_DIR_PATH+"/sub")


######################### AudioIO tests

def test_audio_io_read_streams() -> bool:
    """
    Tests the read streams method in audioIO.

    Tests:
        1. Provide correct input and valid file paths.
        2. Provide empty file_paths dictionary.
        3. Provide invalid file paths
        4. Provide valid file paths with invalid audio formats.

    Returns:
        (bool): True if successful. False otherwise.
    """
    audio = AudioIO()
    return audio.read_streams(
        {"file_1" : WAV_FILE_1_PATH, "file_2" : WAV_FILE_2_PATH}) and \
        audio.read_streams({}) and \
        not audio.read_streams({"file_1" : DESKTOP_OUT_PATH}) and \
        not audio.read_streams({"file_1" : VIDEO_FILE_MP4_PATH})

def test_audio_io_record_stream() -> bool:
    """
    Tests the record_stream method in AudioIO

    Tests:
        1. Record a valid file 
        2. Record with a negative duration.
    """
    audio = AudioIO() 
    io = IO()
    return audio.record_stream("recorded",5) and \
        audio.set_output_paths({"recorded" : TEST_EMPTY_DIR_PATH}) and \
        audio.write(["recorded"]) and \
        not audio.record_stream("recorded",0) and \
        not audio.record_stream("recorded",-5) and \
        io.delete(TEST_EMPTY_DIR_PATH + "/recorded.wav")

def test_audio_io_is_readable() -> bool:
    """
    Tests the is_readable method in audioIO.

    Tests:
        1. Use a valid audio file.
        2. Use a file with a format that is not supported.
        3. Use a directory path. 

    Returns:
        (bool): True if successful. False otherwise.
    """
    audio = AudioIO()
    return audio.is_readable(WAV_FILE_1_PATH) and \
        not audio.is_readable(VIDEO_FILE_AVI_PATH) and \
        not audio.is_readable(TEST_DIR_PATH) 

def test_audio_io_get_stream_configurations() -> bool:
    """
    Tests the get_stream_configurations method in AudioIO.

    Tests: 
        1. Simply call the method.
    
    Returns:
        (bool): True if successful. False otherwise.
    """
    audio = AudioIO()
    audio.read_streams(
        {"file_1" : WAV_FILE_1_PATH, "file_2" : WAV_FILE_2_PATH})
    audio.get_stream_configurations()
    return True

def test_audio_io_get_stream_names() -> bool:
    """
    Tests the get_stream_name method in AudioIO.

    Tests:
        1. Read one valid file and check names.
        2. Read one valid and one invalid file ane check names.
        3. Read no files and check names.

    Returns:
        (bool): True if successful. False otherwise.
    """
    audio = AudioIO()
    audio.read_streams(
        {"file_1" : WAV_FILE_1_PATH, "file_2" : WAV_FILE_2_PATH})
    names_1 = audio.get_stream_names()
    audio.read_streams(
        {"file_1" : WAV_FILE_1_PATH, "file_2" : DESKTOP_OUT_PATH})
    names_2 = audio.get_stream_names()
    audio.read_streams({})
    names_3 = audio.get_stream_names()
    return names_1 == ["file_1","file_2"] and \
        names_2 == [] and \
        names_3 == []

def test_audio_io_get_streams() -> bool:
    """
    Tests the get_stream method in AudioIO.

    Tests:
        1. Ensure type of all read files is bytes.

    Returns:
        (bool): True if successful. False otherwise.
    """
    audio = AudioIO()
    audio.read_streams(
        {"file_1" : WAV_FILE_1_PATH, "file_2" : WAV_FILE_2_PATH})
    streams = audio.get_streams()
    for stream in streams.values():
        if not type(stream) == bytes:
            return False 
    return True 
    

def test_audio_io_get_supported_input_formats() -> bool:
    """
    Tests get_supported_input_formats method in AudioIO.

    Tests:
        1. Get formats and check against expected formats.

    Returns:
        (bool): True if successful. False otherwise.
    """
    audio = AudioIO()
    return audio.get_supported_input_formats() == ("mp3", "mpeg","opus", "wav")

def test_audio_io_get_supported_output_formats() -> bool:
    """
    Tests get_supported_output_formats method in AudioIO.

    Tests:
        1. Get formats and check against expected formats.

    Returns:
        (bool): True if successful. False otherwise.
    """
    audio = AudioIO()
    return audio.get_supported_output_formats() == ("wav","opus")

def test_audio_io_write() -> bool:
    """
    Tests write method in AudioIO.

    Tests:
        1. Write a valid file in every possible audio format. 
        2. Writing to a valid directory path.
        3. Write but only provide output mappings for some files. 
        4. Write to an invalid directory path.
        5. Try and write a file with a unique identifier that was not read.

    Returns:
        (bool): True if successful. False otherwise.
    """

    audio = AudioIO()
    general = GeneralIO()

    return audio.read_streams(
        {"file_1" : WAV_FILE_1_PATH, "file_2" : WAV_FILE_2_PATH}) and \
        audio.set_output_paths({
            "file_1" : TEST_DIR_PATH, "file_2" : TEST_DIR_PATH}) and \
        audio.write(["file_1","file_2"]) and \
        audio.write(["file_1"]) and \
        not audio.set_output_paths({"file_1" : WAV_FILE_1_PATH}) and \
        not audio.write(["invalid"]) and \
        general.delete(TEST_DIR_PATH + "/file_1.wav") and \
        general.delete(TEST_DIR_PATH + "/file_2.wav")  
 

def test_audio_io_mono_to_stereo() -> bool:
    """
    Tests the mono_to_stereo method in AudioIO.

    Tests:
        1. Use method when less than two streams have been read.
        2. Use method when more than two streams have been read.
        3. Use method with two streams that do not have the same frame count.
        4. Use method with streams that have the same count and write output 
        5. Provide an invalid stereo_dir_path.

    Returns:
        (bool): True if successful. False otherwise.
    """
    audio = AudioIO()
    return audio.read_streams({"file_1" : WAV_FILE_1_PATH }) and \
        not audio.mono_to_stereo()[0] and \
        audio.read_streams(
            {"file_1" : WAV_FILE_1_PATH, 
            "file_2" : WAV_FILE_2_PATH,
            "file_3" : WAV_FILE_3_PATH}) and \
        not audio.mono_to_stereo()[0] and \
        audio.read_streams({
            "file_1" : WAV_FILE_1_PATH, "file_2" : WAV_FILE_2_PATH}) and \
        not audio.mono_to_stereo()[0]

def test_audio_io_stereo_to_mono() -> bool:
    """
    Tests the stereo_to_mono method in AudioIO.

    Tests:
        1. Use method with a non-stereo file.
        2. Use method with a valid stereo file. 
        3. Use method with more than one audio stream read.

    Returns:
        (bool): True if successful. False otherwise.
    """
    audio = AudioIO()
    return audio.read_streams({"file_1" : WAV_FILE_1_PATH}) and \
        not audio.stereo_to_mono()[0] and \
        audio.read_streams({"stereo" : STEREO_FILE_1_PATH}) and \
        audio.stereo_to_mono()[0]  and \
        len(audio.get_stream_names()) == 2 and \
        audio.read_streams({
            "file_1" : WAV_FILE_1_PATH, "file_2" : WAV_FILE_2_PATH}) and \
        not audio.stereo_to_mono()[0] 

def test_audio_io_concat() -> bool:
    """
    Tests the concat method in AudioIO.

    Tests:
        1. Use method with multiple valid mono files read and concat.
        2. Use method with single file read.
        3. Use method with no files read.
        4. Use method with a mono and a stereo file. 

    Returns:
        (bool): True if successful. False otherwise.
    """
    audio = AudioIO()
    general = GeneralIO()
    # Test 1 
    audio.read_streams({
        "file_1" : WAV_FILE_1_PATH,
        "file_2" : WAV_FILE_2_PATH, 
        "file_3" : WAV_FILE_3_PATH})
    s_1, name_1 = audio.concat()
    # Test 2 
    audio.read_streams({"file_1" : WAV_FILE_1_PATH})
    s_2, _ = audio.concat()
    # Test 3 
    audio.read_streams({})
    s_3, _ = audio.concat()
    # Test 4 
    audio.read_streams({
        "mono" : WAV_FILE_1_PATH,
        "stereo" : STEREO_FILE_1_PATH})
    s_4, name_4 = audio.concat()
    audio.set_output_formats({name_4 : TEST_DIR_PATH})
    audio.write([name_4])
    general.delete(TEST_DIR_PATH + "/mono_stereo_concatenated.wav")
    return s_1 and s_2 and not s_3 and s_4 and \
        name_1 == "file_1_file_2_file_3_concatenated" and \
        name_4 == "mono_stereo_concatenated"

def test_audio_io_overlay() -> bool:
    """
    Tests the overlay method in AudioIO

    Tests:
        1. Use method with two streams of different lengths and loop shorter.
        2. Use method with two streams of different lengths without looping.
        3. Use method with two streams of the same length 
        4. Use method with not two files.

    Returns:
        (bool): True if successful. False otherwise.
    """
    audio = AudioIO()
    audio.read_streams(
            {"file_1" : WAV_FILE_1_PATH, "file_2" : WAV_FILE_2_PATH})
    success_1, _ = audio.overlay(loop_shorter_stream=True)
    audio.read_streams(
            {"file_1" : WAV_FILE_1_PATH, "file_2" : WAV_FILE_2_PATH})
    success_2, _ = audio.overlay(loop_shorter_stream=False)
    audio.read_streams(
            {"file_1" : WAV_FILE_1_PATH, "file_2" : WAV_FILE_1_PATH})
    success_3, _ = audio.overlay()
    audio.read_streams({"file_1" : WAV_FILE_1_PATH})
    success_4, _ = audio.overlay()
    return success_1 and success_2 and success_3 and not success_4

def test_audio_io_change_volume() -> bool:
    """
    Tests the change_volume method in AudioIO

    Tests:
        1. Use method to double the volume 
        2. Use method to halve the volume.
        3. Use method with change 0.
        4. Use method with a file name that does not exist.

    Returns:
        (bool): True if successful. False otherwise.
    """
    audio = AudioIO()
    return audio.read_streams({"file_1" : WAV_FILE_1_PATH}) and \
        audio.change_volume({"file_1" : -20}) and \
        audio.change_volume({"file_1" : 20}) and \
        audio.change_volume({"file_1" : 0}) and \
        not audio.change_volume({"invalid" : -20}) 

def test_audio_io_reverse() -> bool:
    """
    Tests the reverse method in AudioIO

    Tests:
        1. Use a valid name to reverse
        2. Use method with a file name that does not exist.

    Returns:
        (bool): True if successful. False otherwise.
    """
    audio = AudioIO()   
    return audio.read_streams({"file_1" : WAV_FILE_1_PATH}) and \
        audio.reverse(["file_1"]) and \
        not audio.reverse(["invalid"]) \


def test_audio_io_chunk() -> bool:
    """
    Tests the chunk method in AudioIO

    Tests:
        1. Use a chunk duration that is less than the file duration.
        2. Use a chunk duration that is greater than the chunk duration.
        3. Use an invalid chunk duration.

    Returns:
        (bool): True if successful. False otherwise.
    """
    audio = AudioIO() 
    audio.read_streams({"file_1" : WAV_FILE_1_PATH})
    s1 , _ = audio.chunk({"file_1" : 60})
    audio.read_streams({"file_1" : WAV_FILE_1_PATH})
    duration = audio.get_stream_configurations()["file_1"]["duration_seconds"]
    s2, _ = audio.chunk({"file_1" : duration})
    audio.read_streams({"file_1" : WAV_FILE_1_PATH})
    s3, _ = audio.chunk({"file_1" : -10})
    return s1 and s2 and not s3


######################### VideoIO tests

def test_video_io_read_streams() -> bool:
    """
    Tests the read streams method in audioIO.

    Tests:
        1. Provide correct input and valid file paths.
        2. Provide empty file_paths dictionary.
        3. Provide invalid file paths
        4. Provide valid file paths with invalid audio formats.

    Returns:
        (bool): True if successful. False otherwise.
    """
    video = VideoIO()
    return video.read_streams({
        "file_1_mp4" : VIDEO_FILE_MP4_PATH, "file_2_mxf" : VIDEO_FILE_MXF_PATH}) and \
        video.read_streams({}) and \
        not video.read_streams({"file_1" : DESKTOP_OUT_PATH}) and \
        not video.read_streams({"file_1" : WAV_FILE_1_PATH})

def test_video_io_is_readable() -> bool:
    """
    Tests the is_readable method in VideoIO.

    Tests:
        1. Use a valid video file.
        2. Use a file with a format that is not supported.
        3. Use a directory path. 

    Returns:
        (bool): True if successful. False otherwise.
    """
    video = VideoIO()
    return not video.is_readable(WAV_FILE_1_PATH) and \
        video.is_readable(VIDEO_FILE_MP4_PATH) and \
        not video.is_readable(TEST_DIR_PATH)  


def test_video_io_get_stream_names() -> bool:
    """
    Tests the get_stream_name method in VideoIO.

    Tests:
        1. Read one valid file and check names.
        2. Read one valid and one invalid file ane check names.
        3. Read no files and check names.

    Returns:
        (bool): True if successful. False otherwise.
    """
    video = VideoIO()
    video.read_streams({"file_1_mp4" : VIDEO_FILE_MP4_PATH})
    names_1 = video.get_stream_names()
    video.read_streams({
        "file_1_mp4" : VIDEO_FILE_MP4_PATH,
        "invalid" : WAV_FILE_1_PATH})
    names_2 = video.get_stream_names()
    video.read_streams({})
    names_3 = video.get_stream_names()
    return names_1 == ["file_1_mp4"] and names_2 == [] and names_3 == []


def test_video_io_get_supported_formats() -> bool:
    """
    Tests get_supported_formats method in VideoIO.

    Tests:
        1. Get formats and check against expected formats.

    Returns:
        (bool): True if successful. False otherwise.
    """
    video = VideoIO()
    return video.get_supported_formats() == \
         ("mxf","mov","mp4","wmv","flv","avi","swf","m4v")

def test_video_io_write() -> bool:
    """
    Tests the write method in videoIO

    Tests:
        1. Writing to a valid directory path.
        2. Write but only provide output mappings for some files. 
        3. Write to an invalid directory path.
        4. Try and write a file with a unique identifier that was not read.
        5. Write multiple different file formats.

    Returns:
        (bool): True if successful. False otherwise.
    """
    video = VideoIO()
    general = GeneralIO()
    return video.read_streams({
            "mp4_file" : VIDEO_FILE_MP4_PATH,
            "mov_file" : VIDEO_FILE_MOV_PATH,
            "avi_file" : VIDEO_FILE_AVI_PATH }) and \
        video.set_output_paths(
            {"mp4_file" : TEST_DIR_PATH,
            "mov_file" : TEST_DIR_PATH,
            "avi_file" : TEST_DIR_PATH}) and \
        video.write({
            "mp4_file" : VideoWriteTypes.audio,
            "mov_file" : VideoWriteTypes.video,
            "avi_file" : VideoWriteTypes.video_audio}) and \
        video.write({
            "mp4_file" : VideoWriteTypes.audio}) and \
        not video.write({
            "invalid" : VideoWriteTypes.audio}) and \
        general.delete(TEST_DIR_PATH + "/mov_file.mp4") and \
        general.delete(TEST_DIR_PATH + "/avi_file.mp4") and \
        general.delete(TEST_DIR_PATH + "/mp4_file.wav")

######################### ShellIO tests

def test_shell_io_add_command() -> bool:
    """
    Tests the add_command method in ShellIO

    Tests:
        1. Add a valid command.

    Returns:
        (bool): True if successful. False otherwise.
    """
    shell = ShellIO()
    return shell.add_command("command_1","pwd", stdout = None, stdin = None )

def test_shell_io_get_status() -> bool:
    """
    Tests the get_status method in ShellIO

    Tests:
        1. Add a valid command and check status 

    Returns:
        (bool): True if successful. False otherwise.
    """
    shell = ShellIO()
    return shell.add_command("command_1","pwd") and \
        shell.get_status("command_1")[1] == ShellStatus.ready 

def test_shell_io_run_command() -> bool:
    """
    Tests the run_command method in ShellIO

    Tests:
        1. Run a valid command and check status
        3. Run a command that throws an error and check status.

    Returns:
        (bool): True if successful. False otherwise.
    """
    shell = ShellIO()
    shell.add_command("command_1","pwd")
    _ , ready_1 = shell.get_status("command_1")
    shell.run_command("command_1") 
    time.sleep(1) 
    _ , finished_1 = shell.get_status("command_1")
    shell.add_command("command_2","invalid")
    _ , ready_2 = shell.get_status("command_2")
    shell.run_command("command_2") 
    time.sleep(1) 
    _ , error_1 = shell.get_status("command_2")
    return ready_1 == ShellStatus.ready and \
        finished_1 == ShellStatus.finished and \
        ready_2 == ShellStatus.ready and \
        error_1 == ShellStatus.error

######################### IO tests

def test_io_is_directory() -> bool:
    """
    Tests IO class is_directory function.

    Tests
        1. Confirms function returns true when given a path to a directory

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    return io.is_directory(TEST_DIR_PATH) 

def test_io_is_not_directory() -> bool:
    """
    Tests IO class is_directory function.

    Tests
        1. Confirms function returns false when given a path to a file
    
    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    return not io.is_directory(VALID_SAMPLE_JSON_FILE)

def test_io_is_file() -> bool:
    """
    Tests IO class is_file function.

    Tests:
        1. Confirms function returns true when given a path to a file.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    return io.is_file(VALID_SAMPLE_TXT_FILE)

def test_io_is_not_file() -> bool:
    """
    Tests IO class is_file function

    Tests:
        1. Confirms function returns false when given a path to a directory

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    return not io.is_file(TEST_DIR_PATH)

def test_io_num_files_in_empty_dir() -> bool:
    """
    Tests IO class number_of_files_in_directory function.

    Tests:
        1. Confirms function returns sucess with 0 files in directory.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    success, num = io.number_of_files_in_directory(TEST_EMPTY_DIR_PATH, ["pdf"], False)
    return success and num == 0

def test_io_num_files_in_populated_dir() -> bool:
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
    success_pdf, num_pdf = io.number_of_files_in_directory(TEST_SAMPLE_DIR_PATH, ["pdf"], False)
    sucess_jpg, num_jpg = io.number_of_files_in_directory(TEST_SAMPLE_DIR_PATH, ["jpg"], False)
    success_pdf_jpg, num_pdf_jpg = io.number_of_files_in_directory(TEST_SAMPLE_DIR_PATH, ["jpg", "pdf"], False)
    return success_pdf and sucess_jpg and success_pdf_jpg and \
           num_pdf == 1 and num_jpg == 3 and num_pdf_jpg == 4

def test_io_num_files_in_dir_wildcard() -> bool:
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
    success1, num1 = io.number_of_files_in_directory(TEST_EMPTY_DIR_PATH, ["*"], False)
    success2, num2 = io.number_of_files_in_directory(TEST_SAMPLE_DIR_PATH, ["*"], False)
    return success1 and success2 and num1 == 0 and num2 == 4

def test_io_num_files_in_dir_recursive() -> bool:
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
    success1, num_pdf_inner = io.number_of_files_in_directory(TESTS_OUTER_DIR_PATH, ["pdf"], False)
    success2, num_pdf_rec = io.number_of_files_in_directory(TESTS_OUTER_DIR_PATH, ["pdf"], True)
    success3, num_jpg_pdf_inner = io.number_of_files_in_directory(TESTS_OUTER_DIR_PATH, ["pdf", "jpg"], False)
    success4, num_jpg_pdf_rec = io.number_of_files_in_directory(TESTS_OUTER_DIR_PATH, ["pdf", "jpg"], True)
    success5, num_star_inner = io.number_of_files_in_directory(TESTS_OUTER_DIR_PATH, ["*"], False)
    success6, num_star_rec = io.number_of_files_in_directory(TESTS_OUTER_DIR_PATH, ["*"], True)

    return success1 and success2 and success3 and success4 and success5 and \
           success6 and num_pdf_inner == 1 and num_pdf_rec == 2 and \
           num_jpg_pdf_inner == 3 and num_jpg_pdf_rec == 7 and \
           num_star_inner == 3 and num_star_rec == 7
    
def test_io_num_files_in_dir_bad_input() -> bool:
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
    success2, num2 = io.number_of_files_in_directory(TEST_DIR_PATH, ["weird_extension"], False) 
    return not success1 and num1 == None and success2 and num2 == 0


def test_io_names_of_files_in_empty_directory() -> bool:
    """
    Tests IO class path_of_files_in_directory function on empty directory.

    Tests:
        1. Confirms the function returns true and the array of files is empty
           when given a path to an empty dir.
    
    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    success, names = io.path_of_files_in_directory(TEST_DIR_PATH, ["pdf"], False)
    return success and names == []

def test_io_names_of_files_in_populated_dir() -> bool:
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
    success1, names1 = io.path_of_files_in_directory(TEST_SAMPLE_DIR_PATH, ["pdf"], False)
    success2, names2 = io.path_of_files_in_directory(TESTS_OUTER_DIR_PATH, ["pdf"], True)
    return success1 and sorted(names1) == sorted([NORMAN_TEXT]) and \
           success2 and sorted(names2) == sorted([BEE_MOVIE, NORMAN_TEXT])

def test_io_names_of_files_wildcard() -> bool:
    """
    Tests IO class names_of_files_in_directory, recursive option.

    Tests:
        1. Confirms correct names and success of wildcard option non-recursive.
        2. Confirms correct names and success of wildcard option recursive.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    io = IO()
    success1, names1 = io.path_of_files_in_directory(TESTS_OUTER_DIR_PATH, ["*"], False)
    success2, names2 = io.path_of_files_in_directory(TESTS_OUTER_DIR_PATH, ["*"], True)
    return success1 and sorted(names1) == sorted([BEE_MOVIE, PANDA_JPG, RACCOON_JPG]) and \
           success2 and sorted(names2) == sorted([BEE_MOVIE, PANDA_JPG, RACCOON_JPG, KITTEN_JPG, GOAT_JPG, NORMAN_TEXT, BDAY_CAT_JPG])

def test_io_names_of_files_bad_input() -> bool:
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
    success2, names2 = io.path_of_files_in_directory(TEST_DIR_PATH, ["weird_extension"], False) 
    return not success1 and names1 == [] and success2 and names2 == []

def test_io_read_valid_json() -> bool:
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
    return success and data == {"Test_key" : "I am a test string"}

def test_io_read_valid_yaml() -> bool:
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
    return success and data == {'blueberries' : 100}

def test_io_read_valid_text() -> bool:
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
    return success and data == "This is a test text file"

def test_io_read_invalid() -> bool:
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
    return not success1 and data1 == None and not success2 and data2 == None

def test_io_write_existing_json() -> bool:
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
    return not success1

def test_io_is_not_file() -> bool:
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
    success = io.convert_format(VALID_SAMPLE_YAML_FILE, "JSON", TEST_EMPTY_DIR_PATH)
    _, yaml_data = io.read(VALID_SAMPLE_YAML_FILE)
    _, json_data = io.read(TEST_EMPTY_DIR_PATH + "/sample_yaml.JSON")
    io.delete(TEST_EMPTY_DIR_PATH + "/sample_yaml.JSON")
    return success and yaml_data == json_data

def test_io_convert_txt_to_yaml() -> bool:
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
    return not success

def test_io_create_directory() -> bool:
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
    return success and is_dir

def test_io_create_invalid_directory() -> bool:
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
    return not success

def test_io_move_file() -> bool:
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
    success = io.move_file(KITTEN_JPG, TEST_EMPTY_DIR_PATH)
    is_file = io.is_file(TEST_EMPTY_DIR_PATH + "/kitten_tongue.jpg")
    no_orig = not io.is_file(KITTEN_JPG)
    success2 = io.move_file(TEST_EMPTY_DIR_PATH + "/kitten_tongue.jpg", TEST_SAMPLE_DIR_PATH)
    return success and is_file and no_orig and success2

def test_io_copy() -> bool:
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
    success = io.copy(KITTEN_JPG, TEST_EMPTY_DIR_PATH)
    is_copied = io.is_file(TEST_EMPTY_DIR_PATH + "/kitten_tongue.jpg")
    orig_exists = io.is_file(KITTEN_JPG)
    io.delete(TEST_EMPTY_DIR_PATH + "/kitten_tongue.jpg")
    return success and is_copied and orig_exists

def test_io_rename() -> bool:
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
    success = io.rename(KITTEN_JPG,"kitten")
    is_renamed = io.is_file(TEST_SAMPLE_DIR_PATH + "/kitten.jpg")
    success2 = io.rename(TEST_SAMPLE_DIR_PATH + "/kitten.jpg", "kitten_tongue")
    return success and is_renamed and success2

def test_io_record_audio() -> bool:
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
    return io.record_audio(10,"recording",TEST_EMPTY_DIR_PATH)[0] and \
        not io.record_audio(-10,"recording",TEST_EMPTY_DIR_PATH)[0] and \
        not io.record_audio(10,"recording",VALID_SAMPLE_JSON_FILE)[0] and \
        io.delete(TEST_EMPTY_DIR_PATH + "/recording.wav")

def test_io_mono_to_stereo() -> bool:
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
        WAV_FILE_1_PATH,WAV_FILE_1_COPY_PATH, TEST_EMPTY_DIR_PATH)
    return s1 and \
        not io.mono_to_stereo(WAV_FILE_1_PATH,WAV_FILE_2_PATH,TEST_EMPTY_DIR_PATH)[0] and \
        not io.mono_to_stereo(TEST_EMPTY_DIR_PATH,WAV_FILE_1_COPY_PATH,TEST_EMPTY_DIR_PATH)[0] and \
        io.delete("{}/{}.{}".format(TEST_EMPTY_DIR_PATH,name,"wav"))

def test_io_mono_stereo_valid() -> bool:
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
        WAV_FILE_1_PATH,WAV_FILE_1_COPY_PATH, TEST_EMPTY_DIR_PATH)
    is_file = io.is_file("{}/{}.{}".format(TEST_EMPTY_DIR_PATH,name,"wav"))
    deleted = io.delete("{}/{}.{}".format(TEST_EMPTY_DIR_PATH,name,"wav"))
    return s1 and is_file and deleted

# TODO: mismatch in returns here
def test_io_mono_stereo_invalid_frames() -> bool:
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
        WAV_FILE_1_PATH,WAV_FILE_2_PATH,TEST_EMPTY_DIR_PATH)
    return not s1 and name == None

def test_io_mono_stereo_invalid_files() -> bool:
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
        TEST_EMPTY_DIR_PATH,WAV_FILE_1_COPY_PATH,TEST_EMPTY_DIR_PATH)
    is_file = io.is_file("{}/{}.{}".format(TEST_EMPTY_DIR_PATH,name,"wav"))
    return not s1 and name == None

def test_io_stereo_to_mono() -> bool:
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
    s1, identifiers = io.stereo_to_mono(STEREO_FILE_1_PATH,TEST_EMPTY_DIR_PATH)
    s2, _ = io.stereo_to_mono(WAV_FILE_1_COPY_PATH,TEST_EMPTY_DIR_PATH)
    s3, _ = io.stereo_to_mono(TEST_EMPTY_DIR_PATH,TEST_EMPTY_DIR_PATH)
    s4, _ = io.stereo_to_mono(WAV_FILE_1_PATH,WAV_FILE_1_PATH)
    return s1 and not s2 and not s3 and not s4 and \
        io.delete("{}/{}.{}".format(TEST_EMPTY_DIR_PATH,identifiers[0],"wav")) and \
        io.delete("{}/{}.{}".format(TEST_EMPTY_DIR_PATH,identifiers[1],"wav"))

def test_io_stereo_mono_valid() -> bool:
    """
    Tests the stereo_to_mono method in IO with valid data.

    Tests:
        1. Passes valid stereo file to function.
        2. Confirms that call was unsucessful.
    
    Result:
        (bool): True if all the tests pass. False otherwise.   
    """
    io = IO()
    s1, identifiers = io.stereo_to_mono(STEREO_FILE_1_PATH,TEST_EMPTY_DIR_PATH)
    is_file1 = io.is_file("{}/{}.{}".format(TEST_EMPTY_DIR_PATH,identifiers[0],"wav"))
    is_file2 = io.is_file("{}/{}.{}".format(TEST_EMPTY_DIR_PATH,identifiers[1],"wav"))
    deleted1 = io.delete("{}/{}.{}".format(TEST_EMPTY_DIR_PATH,identifiers[0],"wav"))
    deleted2 = io.delete("{}/{}.{}".format(TEST_EMPTY_DIR_PATH,identifiers[1],"wav"))
    return s1 and is_file1 and is_file2 and deleted1 and deleted2

# TODO: (None, None)?
def test_io_stereo_mono_invalid_mono() -> bool:
    """
    Tests the stereo_to_mono method in IO with a mono file.

    Tests:
        1. Passes a mono file for conversion.
        2. Confirms that call was unsuccessful.

    Result:
        (bool): True if all the tests pass. False otherwise.   
    """
    io = IO()
    s1, names = io.stereo_to_mono(WAV_FILE_1_COPY_PATH,TEST_EMPTY_DIR_PATH)
    return not s1 and names == (None, None)

def test_io_stereo_mono_invalid_file() -> bool:
    """
    Tests the stereo_to_mono method in io with a directory.

    Test:
        1. Passes a directory for conversion.
        2. Confirms that call was unsuccessful.
    
    Result:
        (bool): True if all the tests pass. False otherwise.   
    """
    io = IO()
    s1, names = io.stereo_to_mono(TEST_EMPTY_DIR_PATH,TEST_EMPTY_DIR_PATH)
    return not s1 and names == (None, None)

# TODO: (None, None)?
def test_io_stereo_mono_invalid_output_path() -> bool:
    """
    Tests the stereo_to_mono method in io with an invalid output path.

    Tests
        1. Provides invalid output path to function.
        2. Confirms that conversion was unsuccesful.
    
    Result:
        (bool): True if all the tests pass. False otherwise.   
    """
    io = IO()
    s1, names = io.stereo_to_mono(WAV_FILE_1_PATH,WAV_FILE_1_PATH)
    return not s1 and names == (None, None)

def test_io_concat() -> bool:
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
    s1,identifier = io.concat([WAV_FILE_1_PATH, WAV_FILE_2_PATH, WAV_FILE_3_PATH], TEST_EMPTY_DIR_PATH)
    s2, _ = io.concat([WAV_FILE_1_PATH,VIDEO_FILE_MP4_PATH], TEST_EMPTY_DIR_PATH) 
    s3, _ = io.concat([TEST_EMPTY_DIR_PATH,TEST_EMPTY_DIR_PATH],TEST_EMPTY_DIR_PATH) 
    s4, _ = io.concat([WAV_FILE_1_PATH, WAV_FILE_2_PATH, WAV_FILE_3_PATH], WAV_FILE_1_COPY_PATH)
    return s1 and not s2 and not s3 and not s4 and \
        io.delete("{}/{}.{}".format(TEST_EMPTY_DIR_PATH,identifier,"wav"))

def test_io_concat_valid() -> bool:
    """
    Tests the concat method in IO with valid files.

    Tests:
        1. Concat audio files with same extension.
        2. Confirm concat was successful.

    Result:
        (bool): True if all the tests pass. False otherwise.   
    """
    io = IO()
    s1,identifier = io.concat([WAV_FILE_1_PATH, WAV_FILE_2_PATH, WAV_FILE_3_PATH], TEST_EMPTY_DIR_PATH)
    is_file = io.is_file("{}/{}.{}".format(TEST_EMPTY_DIR_PATH,identifier,"wav"))
    deleted = io.delete("{}/{}.{}".format(TEST_EMPTY_DIR_PATH,identifier,"wav"))
    return s1 and is_file and deleted

def test_io_concat_invalid_extensions() -> bool:
    """
    Tests the concat method in IO with invalid extensions.

    Tests:
        1. Concat audio files with different extensions.
        2. Confirm concat was unsuccessful.

    Result:
        (bool): True if all the tests pass. False otherwise.   
    """
    io = IO()
    s1, name = io.concat([WAV_FILE_1_PATH,VIDEO_FILE_MP4_PATH], TEST_EMPTY_DIR_PATH) 
    return not s1 and name == None

def test_io_concat_invalid_files() -> bool:
    """
    Tests the concat method with invalid non-audio files (directories).

    Tests:
        1. Passes directories to concat.
        2. Confirms concat was unsucessful.
    
    Result:
        (bool): True if all the tests pass. False otherwise.   
    """
    io = IO()
    s1, name = io.concat([TEST_EMPTY_DIR_PATH,TEST_EMPTY_DIR_PATH],TEST_EMPTY_DIR_PATH) 
    return not s1 and name == None

# TODO: return not none here -- test2a_test2b_test_concatenated
def test_io_concat_invalid_output() -> bool:
    """
    Tests the concat method with a bad output directory path.

    Tests:
        1. Passes a file as output directory.
        2. Confirms concat was unsucessful.

    Result:
        (bool): True if all the tests pass. False otherwise.   
    """
    io = IO()
    s1, name = io.concat([WAV_FILE_1_PATH, WAV_FILE_2_PATH, WAV_FILE_3_PATH], WAV_FILE_1_COPY_PATH)
    return not s1 and name == None

def test_io_overlay() -> bool:
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
    s2, _ = io.overlay([WAV_FILE_1_PATH,VIDEO_FILE_MP4_PATH],TEST_EMPTY_DIR_PATH)
    s3, _ = io.overlay([WAV_FILE_1_PATH, WAV_FILE_2_PATH, WAV_FILE_3_PATH], TEST_EMPTY_DIR_PATH) 
    s4, _ = io.overlay([WAV_FILE_1_PATH, WAV_FILE_2_PATH], WAV_FILE_1_PATH)
    return s1 and not s2 and not s3 and not s4 and \
        io.delete("{}/{}.{}".format(TEST_EMPTY_DIR_PATH,identifier,"wav"))

def test_io_overlay_valid() -> bool:
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
    is_file = io.is_file("{}/{}.{}".format(TEST_EMPTY_DIR_PATH,identifier,"wav"))
    deleted = io.delete("{}/{}.{}".format(TEST_EMPTY_DIR_PATH,identifier,"wav"))
    return s1 and is_file and deleted

def test_io_overlay_invalid_video() -> bool:
    """
    Tests the overlay method in IO with an invalid video file.

    Tests:
        1. Attempt to overlay with a video file.
        2. Confirm overlay was unsucessful.
    
    Result:
        (bool): True if all the tests pass. False otherwise.   
    """
    io = IO()
    s1, name = io.overlay([WAV_FILE_1_PATH,VIDEO_FILE_MP4_PATH],TEST_EMPTY_DIR_PATH)
    return not s1 and name == None

def test_io_overlay_invalid_num_files() -> bool:
    """
    Tests the overlay method in IO with an invalid number of files.

    Tests:
        1. Attempts to overlay three files.
        2. Confirm that overlay was unsuccesful.

    Result:
        (bool): True if all the tests pass. False otherwise.   
    """
    io = IO()
    s1, name = io.overlay([WAV_FILE_1_PATH, WAV_FILE_2_PATH, WAV_FILE_3_PATH], TEST_EMPTY_DIR_PATH) 
    return not s1 and name == None

# TODO: name is not None, test2a_test2b_overlaid
def test_io_overlay_invalid_output_dir() -> bool:
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
    return not s1 and name == None

# TODO: documentation is wrong for test
def test_io_change_volume() -> bool:
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
    s2 = io.change_volume(WAV_FILE_1_PATH,-20,TEST_EMPTY_DIR_PATH)
    s3 = io.change_volume(VIDEO_FILE_MP4_PATH,100,TEST_EMPTY_DIR_PATH)
    s4 = io.change_volume(WAV_FILE_1_PATH, 20, WAV_FILE_1_PATH) 
    return s1 and s2 and not s3 and not s4 and \
        io.delete("{}/{}".format(TEST_EMPTY_DIR_PATH,name))

def test_io_reverse_audio() -> bool:
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
    s3 = io.reverse_audio(WAV_FILE_2_PATH,WAV_FILE_2_PATH)
    return s1 and not s2 and not s3 and \
        io.delete("{}/{}".format(TEST_EMPTY_DIR_PATH,name))

def test_io_reverse_valid() -> bool:
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
    is_file = io.is_file("{}/{}".format(TEST_EMPTY_DIR_PATH,name))
    deleted = io.delete("{}/{}".format(TEST_EMPTY_DIR_PATH,name))
    return s1 and is_file and deleted

def test_io_reverse_invalid_input() -> bool:
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
    is_empty = io.number_of_files_in_directory(TEST_EMPTY_DIR_PATH, ["*"], True)[1] == 0
    return not s1 and is_empty

def test_io_reverse_invalid_output() -> bool:
    """
    Tests reverse method with invalid output path.

    Tests:
        1. Passes file as output path.
        2. Confirms that rever was unsuccessful.

    Result:
        (bool): True if all the tests pass. False otherwise.   
    """
    io = IO()
    s1 = io.reverse_audio(WAV_FILE_2_PATH,WAV_FILE_2_PATH)
    is_empty = io.number_of_files_in_directory(TEST_EMPTY_DIR_PATH, ["*"], True)[1] == 0
    return not s1 and is_empty

def test_io_chunk() -> bool:
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
    s1 = io.chunk(WAV_FILE_1_PATH,dir_path,10)
    s2 = io.chunk(VIDEO_FILE_MP4_PATH,dir_path,10)
    s3 = io.chunk(WAV_FILE_1_PATH,dir_path,-10)
    s4 = io.chunk(WAV_FILE_1_PATH,WAV_FILE_1_COPY_PATH,10)
    return s1 and not s2 and not s3 and not s4 and \
        io.delete(dir_path)

def test_io_extract_video_from_file() -> bool:
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
    return  io.extract_video_from_file(VIDEO_FILE_MOV_PATH, TEST_EMPTY_DIR_PATH) and \
        io.is_file("{}/{}".format(TEST_EMPTY_DIR_PATH,name)) and \
        io.delete("{}/{}".format(TEST_EMPTY_DIR_PATH,name)) and \
        not io.extract_video_from_file(WAV_FILE_1_COPY_PATH, TEST_EMPTY_DIR_PATH) and \
        not io.extract_video_from_file(VIDEO_FILE_MOV_PATH, WAV_FILE_1_PATH)

def test_io_extract_video_from_file_not_movie() -> bool:
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
    return not s1

def test_io_extract_video_from_file_bad_dir() -> bool:
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
    return not s1

def test_io_extract_audio_from_file() -> bool:
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
    return io.extract_audio_from_file(VIDEO_FILE_MOV_PATH, TEST_EMPTY_DIR_PATH) and \
        io.is_file(TEST_EMPTY_DIR_PATH + "/sample-mov-file.wav") and \
        io.delete(TEST_EMPTY_DIR_PATH + "/sample-mov-file.wav") and \
        not io.extract_audio_from_file(WAV_FILE_1_PATH, TEST_EMPTY_DIR_PATH) and \
        not io.extract_audio_from_file(VIDEO_FILE_MOV_PATH, VIDEO_FILE_AVI_PATH) 

def test_io_extract_audio_from_file_not_movie() -> bool:
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
    return not s1

def test_io_extract_audio_from_file_bad_dir() -> bool:
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
    return not s1

def test_io_run_shell_command() -> bool:
    """
    Tests the run_shell_command method in IO.

    Tests:
        1. Run a valid shell command 
        2. Run an invalid shell command
    
    Result:
        (bool): True if all the tests pass. False otherwise.   
    """
    io = IO()
    return io.run_shell_command("pwd",None,None)[0] and \
        io.run_shell_command("invalid",None,None)[0]

def test_io_get_shell_process_status() -> bool:
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
    return s1 and s2 and \
        io.get_shell_process_status(identifier_valid) == "finished" and \
        io.get_shell_process_status(identifier_invalid) == "error"

def test_io_get_size() -> bool:
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
    return io.get_size(WAV_FILE_1_PATH)[0] and \
        io.get_size(TEST_DIR_PATH)[0] and \
        not io.get_size("INvalid/path")[0]

def test_io_get_name() -> bool:
    """
    Tests the get_name method in IO.

    Tests:
        1. Get the name of a valid file
        2. Get the name of a valid directory.
    
    Result:
        (bool): True if all the tests pass. False otherwise.   
    """
    io = IO()
    return io.get_name(WAV_FILE_1_PATH) == "test2a" and \
        io.get_name(TEST_EMPTY_DIR_PATH) == "Test-directory"

def test_io_get_file_extension() -> bool:
    """
    Tests the get_file_extension method in IO.

    Tests:
        1. Get extension of a valid file.
        2. Get extension of a directory.
    
    Result:
        (bool): True if all the tests pass. False otherwise.   
    """
    io = IO()
    return io.get_file_extension(WAV_FILE_1_PATH)[1] == "wav" and \
        not io.get_file_extension(TEST_EMPTY_DIR_PATH)[0]

####################### TEST SUITE DEFINITION ################################

def define_io_test_suite() -> TestSuite:
    """
    Creates a test suite for io and adds tests to the suite.

    Returns:
        (TestSuite): Suite containing network tests
    """
    suite = TestSuite()
    #### GeneralIO tests
    suite.add_test("test_general_io_is_directory",(), True, True, 
      test_general_io_is_directory)
    suite.add_test("test_general_io_is_file",(), True, True, 
      test_general_io_is_file)
    suite.add_test("test_general_io_num_files_in_directory",(), True, True, 
      test_general_io_num_files_in_directory)
    suite.add_test("test_general_io_path_of_files_in_directory",(), True, True, 
      test_general_io_path_of_files_in_directory)
    suite.add_test("test_general_io_is_readable", (), True, True, 
       test_general_io_is_readable)
    suite.add_test("test_general_io_get_file_extension", (), True, True, 
       test_general_io_get_file_extension)
    suite.add_test("test_general_io_read_files",(), True, True, 
      test_general_io_read_files)
    suite.add_test("test_general_io_write_to_file",(), True, True, 
      test_general_io_write_to_file)    
    suite.add_test("test_general_io_create_directory",(), True, True, 
      test_general_io_create_directory)   
    suite.add_test("test_general_io_move_file",(), True, True, 
      test_general_io_move_file)   
    suite.add_test("test_general_io_copy",(), True, True, 
      test_general_io_copy)   
    suite.add_test("test_general_io_rename", (), True, True, 
       test_general_io_rename)
    suite.add_test("test_general_io_delete",(), True, True, 
      test_general_io_delete) 

    ## AudioIO tests
    suite.add_test("test_audio_io_read_streams",(),True,True,
              test_audio_io_read_streams)
    suite.add_test("test_audio_io_record_stream", (), True, True, 
       test_audio_io_record_stream)
    suite.add_test("test_audio_io_is_readable",(),True,True,
              test_audio_io_is_readable)
    suite.add_test("test_audio_io_get_stream_configurations",
      (),True,True,test_audio_io_get_stream_configurations)
    suite.add_test("test_audio_io_get_stream_names", (), True, True,
      test_audio_io_get_stream_names)
    suite.add_test("test_audio_io_get_streams", (), True, True, 
      test_audio_io_get_streams)
    suite.add_test("test_audio_io_get_supported_input_formats", (), True, True, 
      test_audio_io_get_supported_input_formats)
    suite.add_test("test_audio_io_get_supported_output_formats", (), True, True, 
      test_audio_io_get_supported_output_formats)
    suite.add_test("test_audio_io_write", (), True, True, test_audio_io_write)
    suite.add_test("test_audio_io_mono_to_stereo", (), True, True, 
      test_audio_io_mono_to_stereo)
    suite.add_test("test_audio_io_stereo_to_mono", (), True, True, 
     test_audio_io_stereo_to_mono)
    suite.add_test("test_audio_io_concat", (), True, True, test_audio_io_concat)
    suite.add_test("test_audio_io_overlay", (), True, True, 
      test_audio_io_overlay)
    suite.add_test("test_audio_io_change_volume", (), True, True, 
      test_audio_io_change_volume)
    suite.add_test("test_audio_io_reverse", (), True, True, 
      test_audio_io_reverse)
    suite.add_test("test_audio_io_chunk", (), True, True, test_audio_io_chunk)

    ## VideoIO tests
    suite.add_test("test_video_io_read_streams", (), True, True, 
      test_video_io_read_streams)
    suite.add_test("test_video_io_is_readable",(),True,True,
              test_video_io_is_readable)
    suite.add_test("test_video_io_get_stream_names", (), True, True, 
      test_video_io_get_stream_names)
    suite.add_test("test_video_io_get_supported_formats", (), True, True, 
      test_video_io_get_supported_formats)
    suite.add_test("test_video_io_write", (), True, True, 
      test_video_io_write)
    
    ## ShellIO tests
    suite.add_test("test_shell_io_add_command",(), True, True, 
      test_shell_io_add_command) 
    suite.add_test("test_shell_io_get_status",(), True, True, 
      test_shell_io_get_status) 
    suite.add_test("test_shell_io_run_command",(), True, True, 
      test_shell_io_run_command)

    ### IO tests
    suite.add_test("test_io_is_directory",(), True, True, 
        test_io_is_directory)
    suite.add_test("test_io_is_not_directory",(), True, True, 
        test_io_is_not_directory)
    suite.add_test("test_io_is_file",(), True, True, test_io_is_file)
    suite.add_test("test_io_is_not_file",(), True, True, test_io_is_not_file)
    suite.add_test("test_io_num_files_in_empty_dir",(), True, True, 
        test_io_num_files_in_empty_dir)
    suite.add_test("test_io_num_files_in_populated_dir",(), True, True, 
        test_io_num_files_in_populated_dir)
    suite.add_test("test_io_num_files_in_dir_wildcard",(), True, True, 
        test_io_num_files_in_dir_wildcard)
    suite.add_test("test_io_num_files_in_dir_recursive",(), True, True, 
        test_io_num_files_in_dir_recursive)
    suite.add_test("test_io_names_of_files_in_empty_directory",(), True, True, 
        test_io_names_of_files_in_empty_directory)
    suite.add_test("test_io_names_of_files_in_populated_dir",(), True, True, 
        test_io_names_of_files_in_populated_dir)
    suite.add_test("test_io_names_of_files_wildcard",(), True, True, 
        test_io_names_of_files_wildcard)
    suite.add_test("test_io_num_files_in_dir_bad_input",(), True, True, 
        test_io_num_files_in_dir_bad_input)
    suite.add_test("test_io_names_of_files_bad_input",(), True, True, 
        test_io_names_of_files_bad_input)
    suite.add_test("test_io_read_valid_json",(), True, True, 
        test_io_read_valid_json)
    suite.add_test("test_io_read_valid_yaml",(), True, True, 
        test_io_read_valid_yaml)
    suite.add_test("test_io_read_valid_text",(), True, True, 
        test_io_read_valid_text)
    suite.add_test("test_io_read_invalid",(), True, True, 
        test_io_read_invalid)
    suite.add_test("test_io_write_existing_json",(), True, True, test_io_write_existing_json)
    suite.add_test("test_io_convert_txt_to_yaml",(), True, True, 
        test_io_convert_txt_to_yaml)
    suite.add_test("test_io_create_directory",(), True, True, 
        test_io_create_directory)
    suite.add_test("test_io_create_invalid_directory",(), True, True, 
        test_io_create_invalid_directory)
    suite.add_test("test_io_move_file",(), True, True, 
        test_io_move_file)
    suite.add_test("test_io_copy",(), True, True, test_io_copy)
    suite.add_test("test_io_rename",(), True, True, test_io_rename)
    suite.add_test("test_io_record_audio",(), True, True,test_io_record_audio)
    suite.add_test("test_io_mono_to_stereo",(), True, True,test_io_mono_to_stereo)
    suite.add_test("test_io_mono_stereo_valid",(), True, True,test_io_mono_stereo_valid)
    suite.add_test("test_io_mono_stereo_invalid_frames",(), True, True,test_io_mono_stereo_invalid_frames)
    suite.add_test("test_io_mono_stereo_invalid_files",(), True, True,test_io_mono_stereo_invalid_files)
    suite.add_test("test_io_stereo_to_mono",(), True, True,test_io_stereo_to_mono)
    suite.add_test("test_io_stereo_mono_valid",(), True, True,test_io_stereo_mono_valid)
    suite.add_test("test_io_stereo_mono_invalid_mono",(), True, True,test_io_stereo_mono_invalid_mono)
    suite.add_test("test_io_stereo_mono_invalid_file",(), True, True,test_io_stereo_mono_invalid_file)
    suite.add_test("test_io_stereo_mono_invalid_output_path",(), True, True,test_io_stereo_mono_invalid_output_path)
    suite.add_test("test_io_concat",(), True, True, test_io_concat)
    suite.add_test("test_io_concat_valid",(), True, True, test_io_concat_valid)
    suite.add_test("test_io_concat_invalid_extensions",(), True, True, test_io_concat_invalid_extensions)
    suite.add_test("test_io_concat_invalid_files",(), True, True, test_io_concat_invalid_files)
    suite.add_test("test_io_concat_invalid_output",(), True, True, test_io_concat_invalid_output)
    suite.add_test("test_io_overlay",(), True, True, test_io_overlay)
    suite.add_test("test_io_overlay_valid",(), True, True, test_io_overlay_valid)
    suite.add_test("test_io_overlay_invalid_video",(), True, True, test_io_overlay_invalid_video)
    suite.add_test("test_io_overlay_invalid_num_files",(), True, True, test_io_overlay_invalid_num_files)
    suite.add_test("test_io_overlay_invalid_output_dir",(), True, True, test_io_overlay_invalid_output_dir)
    suite.add_test("test_io_change_volume",(), True, True, 
       test_io_change_volume)
    suite.add_test("test_io_reverse_audio",(), True, True, 
       test_io_reverse_audio)
    suite.add_test("test_io_reverse_valid",(), True, True, 
       test_io_reverse_valid)
    suite.add_test("test_io_reverse_invalid_input",(), True, True, 
       test_io_reverse_invalid_input)
    suite.add_test("test_io_reverse_invalid_output",(), True, True, 
       test_io_reverse_invalid_output)  
    suite.add_test("test_io_chunk",(), True, True, test_io_chunk)
    suite.add_test("test_io_extract_video_from_file",(), True, True, 
        test_io_extract_video_from_file)
    suite.add_test("test_io_extract_video_from_file_not_movie",(), True, True, 
        test_io_extract_video_from_file_not_movie)
    suite.add_test("test_io_extract_video_from_file_bad_dir",(),True,True,
        test_io_extract_video_from_file_bad_dir)
    suite.add_test("test_io_extract_audio_from_file",(), True, True,
        test_io_extract_audio_from_file)
    suite.add_test("test_io_extract_audio_from_file_not_movie",(), True, True,
        test_io_extract_audio_from_file_not_movie)
    suite.add_test("test_io_extract_audio_from_file_bad_dir",(), True, True,
        test_io_extract_audio_from_file_bad_dir)
    suite.add_test("test_io_extract_audio_from_file_bad_dir",(), True, True,
        test_io_extract_audio_from_file_bad_dir)
    suite.add_test("test_io_run_shell_command",(), True, True, 
        test_io_run_shell_command)
    suite.add_test("test_io_get_shell_process_status",(), True, True,
       test_io_get_shell_process_status)
    suite.add_test("test_io_get_size", (), True, True, test_io_get_size)
    suite.add_test("test_io_get_name", (), True, True, test_io_get_name)
    suite.add_test("test_io_get_file_extension", (), True, True, 
        test_io_get_file_extension)

    return suite 
