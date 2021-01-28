"""
Testing script for the IO component.
"""
# Standard library imports 
import os 
import time
# Local imports 

# Third party imports 
from Src.Components.io import Media, AudioIO, VideoIO, VideoWriteTypes,\
                         GeneralIO, ShellIO, ShellStatus
from ..suites import TestSuite, TestSuiteAttributes

############################### GLOBALS #####################################

WAV_FILE_1_PATH = "Test_files/Media/test2a.wav"
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
VALID_SAMPLE_YAML_FILE = "Test_files/Others/sample_yaml.yaml"
VALID_TEST_DIR_PATH = "Test_files/Others/Test-directory"

########################## TEST DEFINITIONS ##################################


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
        not audio.is_readable(VALID_TEST_DIR_PATH) 

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
    

def test_audio_io_get_supported_formats() -> bool:
    """
    Tests get_supported_formats method in AudioIO.

    Tests:
        1. Get formats and check against expected formats.

    Returns:
        (bool): True if successful. False otherwise.
    """
    audio = AudioIO()
    return audio.get_supported_formats() == ("mp3", "mpeg","opus", "wav")

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
    audio.read_streams({"file_1" : WAV_FILE_1_PATH, "file_2" : WAV_FILE_2_PATH})
    audio.write(
            {"file_1" : 
                {"output_path" : DESKTOP_OUT_PATH, "output_format" : "mp3"},
            "file_1" : 
                {"output_path" : DESKTOP_OUT_PATH, "output_format" : "mp3"}})
            
    return True             




    return audio.read_streams(
            {"file_1" : WAV_FILE_1_PATH, "file_2" : WAV_FILE_2_PATH}) and \
        audio.write(
            {"file_1" : DESKTOP_OUT_PATH, "file_2" : DESKTOP_OUT_PATH}) and \
        audio.write({"file_1" : DESKTOP_OUT_PATH}) and \
        not audio.write(
            {"file_1" : WAV_FILE_1_PATH, "file_2" : WAV_FILE_2_PATH}) and \
        not audio.write({"invalid_id" : DESKTOP_OUT_PATH}) and \
        general.delete("{}/{}".format(DESKTOP_OUT_PATH,"file_1.wav")) and \
        general.delete("{}/{}".format(DESKTOP_OUT_PATH,"file_2.wav"))

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
    general = GeneralIO()
    return audio.read_streams({"file_1" : WAV_FILE_1_PATH }) and \
        not audio.mono_to_stereo()[0] and \
        audio.read_streams(
            {"file_1" : WAV_FILE_1_PATH, 
            "file_2" : WAV_FILE_2_PATH,
            "file_3" : WAV_FILE_3_PATH}) and \
        not audio.mono_to_stereo()[0] and \
        audio.read_streams({
            "file_1" : WAV_FILE_1_PATH, "file_2" : WAV_FILE_2_PATH}) and \
        not audio.mono_to_stereo()[0] and \
        audio.read_streams({
            "file_1" : WAV_FILE_1_PATH, "file_2" : WAV_FILE_1_PATH}) and \
        audio.write({audio.mono_to_stereo()[1] : DESKTOP_OUT_PATH}) and \
        general.delete("{}/{}".format(DESKTOP_OUT_PATH,"file_1_file_2_stereo.wav"))

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
        audio.stereo_to_mono()[0] and \
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
    audio.write(
        {name_4 : DESKTOP_OUT_PATH})
    general.delete(DESKTOP_OUT_PATH + "/mono_stereo_concatenated.wav")
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
    success_1, name_1 = audio.overlay(loop_shorter_stream=True)
    audio.read_streams(
            {"file_1" : WAV_FILE_1_PATH, "file_2" : WAV_FILE_2_PATH})
    success_2, name_2 = audio.overlay(loop_shorter_stream=False)
    audio.read_streams(
            {"file_1" : WAV_FILE_1_PATH, "file_2" : WAV_FILE_1_PATH})
    success_3, name_3 = audio.overlay()
    audio.read_streams({"file_1" : WAV_FILE_1_PATH})
    success_4, name_4 = audio.overlay()
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
        not audio.reverse(["invalid"])

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
        not video.is_readable(VALID_TEST_DIR_PATH)  


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
        video.write({
            "mp4_file" : {
                "path" : DESKTOP_OUT_PATH, 
                "type" : VideoWriteTypes.audio},
            "mov_file" : {
                "path" : DESKTOP_OUT_PATH, 
                "type" : VideoWriteTypes.video},
            "avi_file" : {
                "path" : DESKTOP_OUT_PATH, 
                "type" : VideoWriteTypes.video_audio}}) and \
        video.write({
            "mp4_file" : {
                "path" : DESKTOP_OUT_PATH, 
                "type" : VideoWriteTypes.audio}}) and \
        not video.write({
            "mp4_file" : {
                "path" : WAV_FILE_1_PATH, 
                "type" : VideoWriteTypes.audio}}) and \
        not video.write({
            "invalid" : {
                "path" : WAV_FILE_1_PATH, 
                "type" : VideoWriteTypes.audio}}) and \
        general.delete(DESKTOP_OUT_PATH + "/mov_file.mp4") and \
        general.delete(DESKTOP_OUT_PATH + "/avi_file.mp4") and \
        general.delete(DESKTOP_OUT_PATH + "/mp4_file.wav")
 
######################### GeneralIO tests
# TODO: Need to add more in-depth tests for GeneralIO

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
    return general.is_directory(DESKTOP_OUT_PATH) and \
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
    return not general.is_file(DESKTOP_OUT_PATH) and \
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
    return general.number_of_files_in_directory(DESKTOP_OUT_PATH)[1] == 15 and \
        not general.number_of_files_in_directory(WAV_FILE_1_PATH)[0] and \
        general.number_of_files_in_directory(DESKTOP_OUT_PATH,["pdf"])[1] == 4 and \
        general.number_of_files_in_directory(DESKTOP_OUT_PATH,[".asjkd.j"])[1] == 0 and \
        general.number_of_files_in_directory(DESKTOP_OUT_PATH,["pdf"],True)[1] == 7

def test_general_io_names_of_file_in_directory() -> bool:
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
    return general.names_of_file_in_directory(DESKTOP_OUT_PATH)[0] and \
        not general.names_of_file_in_directory(WAV_FILE_1_PATH)[0] and \
        general.names_of_file_in_directory(DESKTOP_OUT_PATH,["pdf"])[0] and \
        general.number_of_files_in_directory(DESKTOP_OUT_PATH,[".asjkd.j"])[1] == 0 and \
        general.number_of_files_in_directory(DESKTOP_OUT_PATH,["pdf"],True)[0]

def test_general_io_read_files() -> bool:
    """
    Tests the read_file method in GeneralIO

    Tests:
        1. Read a valid json file.
        2. Read a text file.
        3. Read a yaml file.
        4. Read a file with a format that is valid but inconsistent with the 
            file. Ex: yaml file but format is json.
        5. Read an invalid format. 
        6. Read from an invalid file path.

    Returns:
        (bool): True if successful. False otherwise.
    """
    general = GeneralIO()
    return general.read_file(VALID_SAMPLE_JSON_FILE,"json")[0] and \
        general.read_file(VALID_SAMPLE_TXT_FILE,"txt")[0] and \
        general.read_file(VALID_SAMPLE_YAML_FILE,"yaml")[0] and \
        not general.read_file(VALID_SAMPLE_JSON_FILE,"yaml")[0] and \
        not general.read_file(VIDEO_FILE_AVI_PATH,"txt")[0]

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
    return general.write_to_file(DESKTOP_OUT_PATH+"/json_test.json", "json",
        general.read_file(VALID_SAMPLE_JSON_FILE,"json")[1], True) and \
        general.delete(DESKTOP_OUT_PATH+"/json_test.json") and \
        general.write_to_file(DESKTOP_OUT_PATH+"/yaml_test.yaml", "yaml",
        general.read_file(VALID_SAMPLE_YAML_FILE,"yaml",)[1], True) and \
        general.delete(DESKTOP_OUT_PATH+"/yaml_test.yaml") and \
        general.write_to_file(DESKTOP_OUT_PATH+"/test_test.txt", "txt",
        general.read_file(VALID_SAMPLE_TXT_FILE,"txt")[1], True) and \
        general.delete(DESKTOP_OUT_PATH+"/test_test.txt") and \
        general.write_to_file(DESKTOP_OUT_PATH+"/test_test.txt", "txt",
        general.read_file(VALID_SAMPLE_TXT_FILE,"txt")[1], False) and \
        general.delete(DESKTOP_OUT_PATH+"/test_test.txt") and \
        not general.write_to_file(DESKTOP_OUT_PATH+"/Test/json_test.json","json",
        general.read_file(VALID_SAMPLE_JSON_FILE,"json")[1], True) and \
        not general.write_to_file(DESKTOP_OUT_PATH+"/test_test.apple", "txt",
        general.read_file(VALID_SAMPLE_TXT_FILE,"txt")[1], False)

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
    return general.create_directory(DESKTOP_OUT_PATH+"/test") and \
        not general.create_directory(WAV_FILE_1_PATH) and \
        general.delete(DESKTOP_OUT_PATH+"/test")


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
    return general.copy(WAV_FILE_1_PATH,DESKTOP_OUT_PATH,) and \
        general.copy(VALID_TEST_DIR_PATH,DESKTOP_OUT_PATH+"/copied") and \
        not general.copy(VALID_TEST_DIR_PATH,WAV_FILE_1_PATH) and \
        not general.copy(DESKTOP_OUT_PATH+"invalid",
            DESKTOP_OUT_PATH+"/copied-2") and \
        not general.copy(VALID_TEST_DIR_PATH,DESKTOP_OUT_PATH+"/copied") and \
        general.delete(DESKTOP_OUT_PATH+"/copied") and \
        general.delete(DESKTOP_OUT_PATH + "/" + \
            WAV_FILE_1_PATH[WAV_FILE_1_PATH.rfind("/")+1:])

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
    general.copy(WAV_FILE_1_PATH,VALID_TEST_DIR_PATH)
    # Get the names of all files in that directory and move them
    _, names = general.names_of_file_in_directory(VALID_TEST_DIR_PATH)
    # Move all the files in the test directory.
    for name in names:
        if not general.move_file(name,DESKTOP_OUT_PATH):
            return False 
        # Delete the created files
        general.delete("{}/{}".format(DESKTOP_OUT_PATH,
            name[name.rfind("/")+1:]))
    return True 

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
    general.copy(WAV_FILE_1_PATH,VALID_TEST_DIR_PATH)
    # Create a directory 
    general.create_directory(VALID_TEST_DIR_PATH+"/sub")
    # Delete
    _, names = general.names_of_file_in_directory(
        VALID_TEST_DIR_PATH,["wav"])
    return all([general.delete(name,) for name in names]) and \
        general.delete(VALID_TEST_DIR_PATH+"/sub")

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
    print(error_1)
    return ready_1 == ShellStatus.ready and \
        finished_1 == ShellStatus.finished and \
        ready_2 == ShellStatus.ready and \
        error_1 == ShellStatus.error


####################### TEST SUITE DEFINITION ################################

def define_io_test_suite() -> TestSuite:
    """
    Creates a test suite for io and adds tests to the suite.

    Returns:
        (TestSuite): Suite containing network tests
    """
    suite = TestSuite()
    #### AudioIO tests
    # suite.add_test("test_audio_io_read_streams",(),True,True,
    #             test_audio_io_read_streams)
    # suite.add_test("test_audio_io_is_readable",(),True,True,
    #             test_audio_io_is_readable)
    # suite.add_test("test_audio_io_get_stream_configurations",
    #     (),True,True,test_audio_io_get_stream_configurations)
    # suite.add_test("test_audio_io_get_stream_names", (), True, True,
    #     test_audio_io_get_stream_names)
    # suite.add_test("test_audio_io_get_streams", (), True, True, 
    #     test_audio_io_get_streams)
    # suite.add_test("test_audio_io_get_supported_formats", (), True, True, 
    #     test_audio_io_get_supported_formats)
    suite.add_test("test_audio_io_write", (), True, True, test_audio_io_write)
    # suite.add_test("test_audio_io_mono_to_stereo", (), True, True, 
    #     test_audio_io_mono_to_stereo)
    # suite.add_test("test_audio_io_stereo_to_mono", (), True, True, 
    #    test_audio_io_stereo_to_mono)
    # suite.add_test("test_audio_io_concat", (), True, True, test_audio_io_concat)
    # suite.add_test("test_audio_io_overlay", (), True, True, 
    #     test_audio_io_overlay)
    # suite.add_test("test_audio_io_change_volume", (), True, True, 
    #     test_audio_io_change_volume)
    # suite.add_test("test_audio_io_reverse", (), True, True, 
    #     test_audio_io_reverse)
    # suite.add_test("test_audio_io_chunk", (), True, True, test_audio_io_chunk)
    #### VideoIO tests
    # suite.add_test("test_video_io_read_streams", (), True, True, 
    #     test_video_io_read_streams)
    # suite.add_test("test_video_io_is_readable",(),True,True,
    #             test_video_io_is_readable)
    # suite.add_test("test_video_io_get_stream_names", (), True, True, 
    #     test_video_io_get_stream_names)
    # suite.add_test("test_video_io_get_supported_formats", (), True, True, 
    #     test_video_io_get_supported_formats)
    # suite.add_test("test_video_io_write", (), True, True, 
    #     test_video_io_write)
    #### GeneralIO tests
    # suite.add_test("test_general_io_is_directory",(), True, True, 
    #     test_general_io_is_directory)
    # suite.add_test("test_general_io_is_file",(), True, True, 
    #     test_general_io_is_file)
    # suite.add_test("test_general_io_num_files_in_directory",(), True, True, 
    #     test_general_io_num_files_in_directory)
    # suite.add_test("test_general_io_names_of_file_in_directory",(), True, True, 
    #     test_general_io_names_of_file_in_directory)
    # suite.add_test("test_general_io_read_files",(), True, True, 
    #     test_general_io_read_files)
    # suite.add_test("test_general_io_write_to_file",(), True, True, 
    #     test_general_io_write_to_file)    
    # suite.add_test("test_general_io_create_directory",(), True, True, 
    #     test_general_io_create_directory)   
    # suite.add_test("test_general_io_copy",(), True, True, 
    #     test_general_io_copy)   
    # suite.add_test("test_general_io_move_file",(), True, True, 
    #     test_general_io_move_file)   
    # suite.add_test("test_general_io_delete",(), True, True, 
    #     test_general_io_delete) 
    # # ShellIO tests
    # suite.add_test("test_shell_io_add_command",(), True, True, 
    #     test_shell_io_add_command) 
    # suite.add_test("test_shell_io_get_status",(), True, True, 
    #     test_shell_io_get_status) 
    # suite.add_test("test_shell_io_run_command",(), True, True, 
    #     test_shell_io_run_command)
    return suite 

    test_shell_io_run_command