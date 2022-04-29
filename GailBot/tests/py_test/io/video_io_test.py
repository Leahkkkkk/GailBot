# Standard library imports
import os
# Local imports
from Src.components.io import GeneralIO, VideoIO, VideoWriteTypes
from Tests.io.vardefs import *

############################### GLOBALS #####################################

########################## TEST DEFINITIONS ##################################


def test_video_io_read_streams() -> None:
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
    assert video.read_streams({
        "file_1_mp4": VIDEO_FILE_MP4_PATH, "file_2_mxf": VIDEO_FILE_MXF_PATH}) and \
        video.read_streams({}) and \
        not video.read_streams({"file_1": DESKTOP_OUT_PATH}) and \
        not video.read_streams({"file_1": WAV_FILE_1_PATH})


def test_video_io_is_readable() -> None:
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
    assert not video.is_readable(WAV_FILE_1_PATH) and \
        video.is_readable(VIDEO_FILE_MP4_PATH) and \
        not video.is_readable(TEST_DIR_PATH)


def test_video_io_get_stream_names() -> None:
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
    video.read_streams({"file_1_mp4": VIDEO_FILE_MP4_PATH})
    names_1 = video.get_stream_names()
    video.read_streams({
        "file_1_mp4": VIDEO_FILE_MP4_PATH,
        "invalid": WAV_FILE_1_PATH})
    names_2 = video.get_stream_names()
    video.read_streams({})
    names_3 = video.get_stream_names()
    assert names_1 == ["file_1_mp4"] and names_2 == [] and names_3 == []


def test_video_io_get_supported_formats() -> None:
    """
    Tests get_supported_formats method in VideoIO.

    Tests:
        1. Get formats and check against expected formats.

    Returns:
        (bool): True if successful. False otherwise.
    """
    video = VideoIO()
    assert len(video.get_supported_formats()) > 0


def test_video_io_write() -> None:
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
    assert video.read_streams({
        "mp4_file": VIDEO_FILE_MP4_PATH,
        "mov_file": VIDEO_FILE_MOV_PATH,
        "avi_file": VIDEO_FILE_AVI_PATH}) and \
        video.set_output_paths(
            {"mp4_file": TEST_DIR_PATH,
             "mov_file": TEST_DIR_PATH,
             "avi_file": TEST_DIR_PATH}) and \
        video.write({
            "mp4_file": VideoWriteTypes.audio,
            "mov_file": VideoWriteTypes.video,
            "avi_file": VideoWriteTypes.video_audio}) and \
        video.write({
            "mp4_file": VideoWriteTypes.audio}) and \
        not video.write({
            "invalid": VideoWriteTypes.audio}) and \
        general.delete(TEST_DIR_PATH + "/mov_file.mp4") and \
        general.delete(TEST_DIR_PATH + "/avi_file.mp4") and \
        general.delete(TEST_DIR_PATH + "/mp4_file.wav")
