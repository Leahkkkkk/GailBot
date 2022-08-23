# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-11-30 17:58:28
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-08-23 10:09:41
# Standard library imports
from typing import Dict, List, Any, Tuple
from enum import IntEnum, Enum
# Third party imports
from moviepy.editor import *
# Local imports
from dataclasses import dataclass
from gailbot.utils.threads import ThreadPool


class VideoWriteTypes(IntEnum):
    """
    Defines the different types of write operations that can be performed on
    a VideoStream.

    Attributes:
        video_audio: Includes both video and audio.
        video: Only includes video and not audio.
        audio: Only includes audio and not video.
    """
    video_audio = 0
    video = 1
    audio = 2


@dataclass
class VideoStream:
    input_file_path: str
    input_format: str
    video_clip: VideoFileClip
    output_dir_path: str = None


# TODO: Add functionality to write in different video formats.


class VideoIO:

    # Video formats that are currently supported.
    INPUT_VIDEO_FORMATS = ("mxf", "mov", "mp4", "wmv", "flv", "avi",
                           # "swf",
                           "m4v")
    OUTPUT_VIDEO_FORMATS = ("mp4")
    OUTPUT_AUDIO_FORMATS = ("wav")

    def __init__(self) -> None:
        """
        Params:
            streams (Dict[str,VideoStream]): Mapping from identifier to stream.
            default_video_input_format (str):  Format video files are written in.
            default_audio_output_format (str): Format audio file are written in.
            num_threads (int): No. of threads used by the thread pool.
            thread_pool (ThreadPool): pool that manages all threads.
        """
        # Params
        self.streams: Dict[str, VideoStream] = dict()
        self.default_video_input_format = "mp4"
        self.default_audio_output_format = "wav"
        self.num_threads = 10
        # Starting thread pool
        self.thread_pool = ThreadPool(self.num_threads)
        self.thread_pool.spawn_threads()

    ################################# SETTERS ###############################

    def read_streams(self, file_paths: Dict[str, str]) -> bool:
        """
        Read the audio files at the given paths for future operations.
        Clears all previously read streams from memory.
        Intended to be used after using the write method to save operations
        performed on previous streams.

        Args:
            file_paths (Dict[str,str]):
                Mapping from unique file name to its path.

         Returns:
            (bool): True if all files are successfully read. False otherwise.
        """
        # Clears all the previous streams when reading new ones.
        self.streams.clear()
        # Determine whether all files are valid
        if not all([self._is_video_file(path) for path in file_paths.values()]):
            return False
        # If all files exist, they are read as VideoClip objects.
        for name, file_path in file_paths.items():
            success, stream = self._initialize_video_stream_from_file(
                file_path, self.default_video_input_format, None)
            if not success:
                self.streams.clear()
                return False
            self.streams[name] = stream
        return True

    def set_output_paths(self, output_dir_paths: Dict[str, str]) -> bool:
        """
        Set the output direcotry path for the video streams associated with
        the identifiers

        Args:
            output_dir_paths (Dict[str,str]):
                Mapping from identifier to output directory path.
                The path must be a valid directory path.

        Returns:
            (bool): True if path successfully set. False otherwise.
        """
        # Setting the output paths for each AudioStream
        for name, output_dir_path in output_dir_paths.items():
            # Verify identifiers and path
            if not name in self.streams or \
                    not self._is_directory(output_dir_path):
                return False
            self.streams[name].output_dir_path = output_dir_path
        return True

    ################################# GETTERS #############################

    def is_readable(self, file_path: str) -> bool:
        """
        Determine if the file at the given path is readable by VideoIO.
        """
        return self._is_video_file(file_path)

    def get_stream_names(self) -> List[str]:
        """
        Get the unique identifiers / names of all the files that are currently
        ready to have operations performed on.

        Returns:
            (List): Name of all files in stream.
        """
        return list(self.streams.keys())

    def get_supported_formats(self) -> Tuple[str]:
        """
        Get the video file formats that are supported.

        Returns:
            (Tuple): Supported video file formats
        """
        return tuple(self.INPUT_VIDEO_FORMATS)

    ############################### PUBLIC METHODS ########################

    def write(self, identifiers: Dict[str, VideoWriteTypes]) -> Tuple[bool, Dict]:
        """
        Write the video streams that were previously read as either a file
        containing both audio and video, only video, and only audio.
        Returns a mapping from identifier to output paths

        Args:
            identifiers (Dict[str, VideoWriteTypes]):
                Mapping from the unique identifier to the type of file to write,
                defined by VideoWriteTypes.

        """
        # Create a closure to determine thread success
        paths = dict()
        closure = dict()
        for name in identifiers.keys():
            closure[name] = False
        # Verify all identifiers
        if not all([identifier in self.streams.keys()
                    for identifier in identifiers.keys()]):
            return paths
        # Write all the output files
        for name in identifiers.keys():
            # Determine output type and file name
            output_dir_path = self.streams[name].output_dir_path
            # Write correct type by creating thread.
            output_type = identifiers[name]
            if output_type == VideoWriteTypes.video_audio:
                output_file_name = "{}/{}.{}".format(
                    output_dir_path, name, self.default_video_input_format)
                self.thread_pool.add_task(
                    self._write_video_audio, [name, output_file_name, closure])
            elif output_type == VideoWriteTypes.audio:
                output_file_name = "{}/{}.{}".format(
                    output_dir_path, name, self.default_audio_output_format)
                self.thread_pool.add_task(
                    self._write_audio, [name, output_file_name, closure])
            else:
                output_file_name = "{}/{}.{}".format(
                    output_dir_path, name, self.default_video_input_format)
                self.thread_pool.add_task(
                    self._write_video, [name, output_file_name, closure])
            paths[name] = output_file_name
        # Run and wait for all tasks in the pool to finish
        is_success = self.thread_pool.wait_completion()
        return is_success and all(closure.values()), paths

    ############################# PRIVATE METHODS ###########################

    def _initialize_video_stream_from_file(
            self, input_file_path, input_format,
            output_dir_path) -> Tuple[bool, VideoStream]:
        """
        Initializes and returns an VideoStream object by reading from input
        path.

        Args:
            input_file_path (str): Path to the input video file.
            input_format (input_format): Format to read the input file in.
            output_dir_path (str): Path of the output directory.
        """
        try:
            # The output path defaults to the input path directory if not specified
            if len(input_file_path) > 0 and output_dir_path == None:
                output_dir_path = input_file_path[:input_file_path.rfind("/")]
            # Storing items
            video_clip = VideoFileClip(input_file_path)
            video_stream = VideoStream(
                input_file_path, input_format, video_clip, output_dir_path)
            return (True, video_stream)
        except Exception as e:
            return (False, None)

    # Write methods

    def _write_video_audio(self, name: str, output_file_name: str,
                           closure: Dict[str, bool]):
        """
        Write an output file containing both video and audio.
        Intended to be used as a thread function.

        Args:
            name (str): Unique identifier for the stream.
            output_file_name (str): Name of the output file.
            closure (Dict[str,bool]): Mapping from unique identifier to True
                    if successfully written. False otherwise
        """
        try:
            video_clip = self.streams[name].video_clip
            video_clip.write_videofile(output_file_name)
            closure[name] = True
        except:
            closure[name] = False

    def _write_audio(self, name: str, output_file_name: str,
                     closure: Dict[str, bool]):
        """
        Write an output file containing only audio.
        Intended to be used as a thread function.

        Args:
            name (str): Unique identifier for the stream.
            output_file_name (str): Name of the output file.
            closure (Dict[str,bool]): Mapping from unique identifier to True
                    if successfully written. False otherwise
        """
        try:
            video_clip = self.streams[name].video_clip
            audio = video_clip.audio
            audio.write_audiofile(output_file_name)
            closure[name] = True
        except:
            closure[name] = False

    def _write_video(self, name: str, output_file_name: str,
                     closure: Dict[str, bool]):
        """
        Write an output file containing only video.
        Intended to be used as a thread function.

        Args:
            name (str): Unique identifier for the stream.
            output_file_name (str): Name of the output file.
            closure (Dict[str,bool]): Mapping from unique identifier to True
                    if successfully written. False otherwise
        """
        try:
            video_clip = self.streams[name].video_clip
            video_clip.write_videofile(output_file_name, audio=False)
            closure[name] = True
        except:
            closure[name] = False

    # Others
    def _does_file_exist(self, file_path: str) -> bool:
        """
        Determines if the file exists.
        """
        return os.path.exists(file_path) and os.path.isfile(file_path)

    def _is_video_file(self, file_path: str) -> bool:
        """
        Determines if the is video file
        """
        return self._does_file_exist(file_path) and \
            self._get_file_extension(file_path).lower() in \
            self.INPUT_VIDEO_FORMATS

    def _get_file_extension(self, file_path: str) -> str:
        """
        Obtain file extension /format, which is the substring after the right-
        most "." character.

        """
        return os.path.splitext(file_path.strip())[1][1:]

    def _is_directory(self, dir_path: str) -> bool:
        """
        Determine if path is a directory.
        """
        return os.path.isdir(dir_path)
