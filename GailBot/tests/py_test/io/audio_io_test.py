# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-04-29 15:34:30
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-04-29 15:46:34
# Standard library imports
import os
# Local imports
from src.gailbot.components.io import AudioIO, IO, GeneralIO
from ...vardefs import *
from ...utils import *

############################### GLOBALS #####################################


########################## TEST DEFINITIONS ##################################


def test_audio_io_read_streams() -> None:
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
    assert audio.read_streams(
        {"file_1": WAV_ASSASSINATION_FILE, "file_2": WAV_SINE_FILE}) and \
        audio.read_streams({}) and \
        not audio.read_streams({"file_1": IO_RESULTS}) and \
        not audio.read_streams({"file_1": JPG_KITTEN_TONGUE})


def test_audio_io_record_stream() -> None:
    """
    Tests the record_stream method in AudioIO

    Tests:
        1. Record a valid file
        2. Record with a negative duration.
    """
    audio = AudioIO()
    io = IO()
    assert audio.record_stream("recorded", 5) and \
        audio.set_output_paths({"recorded": IO_RESULTS}) and \
        audio.write(["recorded"]) and \
        not audio.record_stream("recorded", 0) and \
        not audio.record_stream("recorded", -5) and \
        io.delete(IO_RESULTS + "/recorded.wav")


def test_audio_io_is_readable() -> None:
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
    assert audio.is_readable(MP3_ASSASSINATION_FILE) and \
        not audio.is_readable(IO_RESULTS)


def test_audio_io_get_stream_configurations() -> None:
    """
    Tests the get_stream_configurations method in AudioIO.

    Tests:
        1. Simply call the method.

    Returns:
        (bool): True if successful. False otherwise.
    """
    audio = AudioIO()
    audio.read_streams(
        {"file_1": WAV_TEST2B_FILE, "file_2": WAV_TEST2A_FILE})
    audio.get_stream_configurations()


def test_audio_io_get_stream_names() -> None:
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
        {"file_1": WAV_TEST2B_FILE, "file_2": WAV_TEST2A_FILE})
    names_1 = audio.get_stream_names()
    audio.read_streams(
        {"file_1": WAV_TEST2B_FILE, "file_2": IO_RESULTS})
    names_2 = audio.get_stream_names()
    audio.read_streams({})
    names_3 = audio.get_stream_names()
    assert names_1 == ["file_1", "file_2"] and \
        names_2 == [] and \
        names_3 == []


def test_audio_io_get_streams() -> None:
    """
    Tests the get_stream method in AudioIO.

    Tests:
        1. Ensure type of all read files is bytes.

    Returns:
        (bool): True if successful. False otherwise.
    """
    audio = AudioIO()
    audio.read_streams(
        {"file_1": WAV_TEST2B_FILE, "file_2": WAV_TEST2A_FILE})
    streams = audio.get_streams()
    for stream in streams.values():
        assert type(stream) == bytes


def test_audio_io_get_supported_input_formats() -> None:
    """
    Tests get_supported_input_formats method in AudioIO.

    Tests:
        1. Get formats and check against expected formats.

    Returns:
        (bool): True if successful. False otherwise.
    """
    audio = AudioIO()
    assert audio.get_supported_input_formats() == ("mp3", "mpeg", "opus", "wav")


def test_audio_io_get_supported_output_formats() -> None:
    """
    Tests get_supported_output_formats method in AudioIO.

    Tests:
        1. Get formats and check against expected formats.

    Returns:
        (bool): True if successful. False otherwise.
    """
    audio = AudioIO()
    assert audio.get_supported_output_formats() == ("wav", "opus")


def test_audio_io_write() -> None:
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
    assert audio.read_streams(
        {"file_1": WAV_TEST2B_FILE, "file_2": WAV_TEST2A_FILE}) and \
        audio.set_output_paths({
            "file_1": IO_RESULTS, "file_2": IO_RESULTS}) and \
        audio.write(["file_1", "file_2"]) and \
        audio.write(["file_1"]) and \
        not audio.set_output_paths({"file_1": WAV_ASSASSINATION_FILE}) and \
        not audio.write(["invalid"]) and \
        general.delete(IO_RESULTS + "/file_1.wav") and \
        general.delete(IO_RESULTS + "/file_2.wav")


def test_audio_io_mono_to_stereo() -> None:
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
    assert audio.read_streams({"file_1": WAV_TEST2A_FILE}) and \
        not audio.mono_to_stereo()[0] and \
        audio.read_streams(
            {"file_1": WAV_TEST2A_FILE,
             "file_2": WAV_TEST2B_FILE,
             "file_3": WAV_TEST_OUTPUT_FILE}) and \
        not audio.mono_to_stereo()[0] and \
        audio.read_streams({
            "file_1": WAV_TEST2A_FILE, "file_2": WAV_TEST2B_FILE}) and \
        not audio.mono_to_stereo()[0]


def test_audio_io_stereo_to_mono() -> None:
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
    assert audio.read_streams({"file_1": WAV_TEST2A_FILE}) and \
        not audio.stereo_to_mono()[0] and \
        audio.read_streams({"stereo": WAV_TEST_OUTPUT_FILE}) and \
        audio.stereo_to_mono()[0] and \
        len(audio.get_stream_names()) == 2 and \
        audio.read_streams({
            "file_1": WAV_TEST2A_FILE, "file_2": WAV_TEST2B_FILE}) and \
        not audio.stereo_to_mono()[0]


def test_audio_io_concat() -> None:
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
        "file_1": WAV_TEST2A_FILE,
        "file_2": WAV_TEST2B_FILE,
        "file_3": WAV_ASSASSINATION_FILE})
    s_1, name_1 = audio.concat()
    # Test 2
    audio.read_streams({"file_1":  WAV_TEST2A_FILE, })
    s_2, _ = audio.concat()
    # Test 3
    audio.read_streams({})
    s_3, _ = audio.concat()
    # Test 4
    audio.read_streams({
        "mono":  WAV_TEST2A_FILE,
        "stereo": WAV_TEST_OUTPUT_FILE})
    s_4, name_4 = audio.concat()
    audio.set_output_formats({name_4: WAV_TEST_OUTPUT_FILE})
    audio.write([name_4])
    general.delete(IO_RESULTS + "/mono_stereo_concatenated.wav")
    assert s_1 and s_2 and not s_3 and s_4 and \
        name_1 == "file_1_file_2_file_3_concatenated" and \
        name_4 == "mono_stereo_concatenated"


# def test_audio_io_overlay() -> None:
#     """
#     Tests the overlay method in AudioIO

#     Tests:
#         1. Use method with two streams of different lengths and loop shorter.
#         2. Use method with two streams of different lengths without looping.
#         3. Use method with two streams of the same length
#         4. Use method with not two files.

#     Returns:
#         (bool): True if successful. False otherwise.
#     """
#     audio = AudioIO()
#     audio.read_streams(
#         {"file_1": WAV_FILE_1_PATH, "file_2": WAV_FILE_2_PATH})
#     success_1, _ = audio.overlay(loop_shorter_stream=True)
#     audio.read_streams(
#         {"file_1": WAV_FILE_1_PATH, "file_2": WAV_FILE_2_PATH})
#     success_2, _ = audio.overlay(loop_shorter_stream=False)
#     audio.read_streams(
#         {"file_1": WAV_FILE_1_PATH, "file_2": WAV_FILE_1_PATH})
#     success_3, _ = audio.overlay()
#     audio.read_streams({"file_1": WAV_FILE_1_PATH})
#     success_4, _ = audio.overlay()
#     assert success_1 and success_2 and success_3 and not success_4


# def test_audio_io_change_volume() -> None:
#     """
#     Tests the change_volume method in AudioIO

#     Tests:
#         1. Use method to double the volume
#         2. Use method to halve the volume.
#         3. Use method with change 0.
#         4. Use method with a file name that does not exist.

#     Returns:
#         (bool): True if successful. False otherwise.
#     """
#     audio = AudioIO()
#     assert audio.read_streams({"file_1": WAV_FILE_1_PATH}) and \
#         audio.change_volume({"file_1": -20}) and \
#         audio.change_volume({"file_1": 20}) and \
#         audio.change_volume({"file_1": 0}) and \
#         not audio.change_volume({"invalid": -20})


# def test_audio_io_reverse() -> None:
#     """
#     Tests the reverse method in AudioIO

#     Tests:
#         1. Use a valid name to reverse
#         2. Use method with a file name that does not exist.

#     Returns:
#         (bool): True if successful. False otherwise.
#     """
#     audio = AudioIO()
#     assert audio.read_streams({"file_1": WAV_FILE_1_PATH}) and \
#         audio.reverse(["file_1"]) and \
#         not audio.reverse(["invalid"]) \


# def test_audio_io_chunk() -> None:
#     """
#     Tests the chunk method in AudioIO

#     Tests:
#         1. Use a chunk duration that is less than the file duration.
#         2. Use a chunk duration that is greater than the chunk duration.
#         3. Use an invalid chunk duration.

#     Returns:
#         (bool): True if successful. False otherwise.
#     """
#     audio = AudioIO()
#     audio.read_streams({"file_1": WAV_FILE_1_PATH})
#     s1, _ = audio.chunk({"file_1": 60})
#     audio.read_streams({"file_1": WAV_FILE_1_PATH})
#     duration = audio.get_stream_configurations()["file_1"]["duration_seconds"]
#     s2, _ = audio.chunk({"file_1": duration})
#     audio.read_streams({"file_1": WAV_FILE_1_PATH})
#     s3, _ = audio.chunk({"file_1": -10})
#     assert s1 and s2 and not s3
