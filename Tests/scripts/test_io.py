"""
Testing script for the IO component.
"""
# Standard library imports 

# Local imports 

# Third party imports 
from re import A
from Src.Components.io import Media, AudioIO
from ..suites import TestSuite, TestSuiteAttributes

############################### GLOBALS #####################################

WAV_FILE_1_PATH = "/Users/muhammadumair/Documents/Repositories/mumair01-Repos/GailBot-0.3/Test_files/Media/test2a.wav"
WAV_FILE_2_PATH = "/Users/muhammadumair/Documents/Repositories/mumair01-Repos/GailBot-0.3/Test_files/Media/test2b.wav"
WAV_FILE_3_PATH = "/Users/muhammadumair/Documents/Repositories/mumair01-Repos/GailBot-0.3/Test_files/Media/test.wav"
STEREO_FILE_1_PATH = "/Users/muhammadumair/Documents/Repositories/mumair01-Repos/GailBot-0.3/Test_files/Media/SineWaveMinus16.wav"
VIDEO_FILE_1_PATH = "/Users/muhammadumair/Documents/Repositories/mumair01-Repos/GailBot-0.3/Test_files/Media/vid.mp4"
DESKTOP_OUT_PATH = "/Users/muhammadumair/Desktop"

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
        not audio.read_streams({"file_1" : VIDEO_FILE_1_PATH})

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

def test_audio_io_get_supported_formats() -> bool:
    """
    Tests get_supported_formats method in AudioIO.

    Tests:
        1. Get formats and check against expected formats.

    Returns:
        (bool): True if successful. False otherwise.
    """
    audio = AudioIO()
    return audio.get_supported_formats() == \
        ("alaw", "basic", "flaf", "g729", "pcm", "mp3", "mpeg", 
        "ulaw", "opus", "wav", "webm")

def test_audio_io_write() -> bool:
    """
    Tests write method in AudioIO.

    Tests:
        1. Writing to a valid directory path.
        2. Write but only provide output mappings for some files. 
        2. Write to an invalid directory path.
        3. Try and write a file with a unique identifier that was not read.

    Returns:
        (bool): True if successful. False otherwise.
    """
    audio = AudioIO()
    return audio.read_streams(
            {"file_1" : WAV_FILE_1_PATH, "file_2" : WAV_FILE_2_PATH}) and \
        audio.write(
            {"file_1" : DESKTOP_OUT_PATH, "file_2" : DESKTOP_OUT_PATH}) and \
        audio.write({"file_1" : DESKTOP_OUT_PATH}) and \
        not audio.write(
            {"file_1" : WAV_FILE_1_PATH, "file_2" : WAV_FILE_2_PATH}) and \
        not audio.write({"invalid_id" : DESKTOP_OUT_PATH})

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
        not audio.mono_to_stereo()[0] and \
        audio.read_streams({
            "file_1" : WAV_FILE_1_PATH, "file_2" : WAV_FILE_1_PATH}) and \
        audio.write({audio.mono_to_stereo()[1] : DESKTOP_OUT_PATH})

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
    return s_1 and s_2 and not s_3 and s_4 and \
        name_1 == "file_1_file_2_file_3" and \
        name_4 == "mono_stereo"

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
    audio.write({name_1 : DESKTOP_OUT_PATH})
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


####################### TEST SUITE DEFINITION ################################

def define_io_test_suite() -> TestSuite:
    """
    Creates a test suite for io and adds tests to the suite.

    Returns:
        (TestSuite): Suite containing network tests
    """
    suite = TestSuite()
    suite.add_test("test_audio_io_read_streams",(),True,True,
                test_audio_io_read_streams)
    suite.add_test("test_audio_io_get_stream_configurations",
        (),True,True,test_audio_io_get_stream_configurations)
    suite.add_test("test_audio_io_get_stream_names", (), True, True,
        test_audio_io_get_stream_names)
    suite.add_test("test_audio_io_get_supported_formats", (), True, True, 
        test_audio_io_get_supported_formats)
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
    return suite 