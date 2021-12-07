# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-10-19 15:34:24
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2021-12-05 17:04:18
# Standard library imports
import os
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
# Local imports
# Third party imports
from pydub import AudioSegment
from copy import deepcopy
import sounddevice as sd


@dataclass
class AudioStream:
    input_file_path: str
    input_format: str
    audio_segment: AudioSegment
    output_dir_path: str
    output_format: str


class AudioIO:
    """
    Provides methods that directly interact with and can modify audio streams
    and files. Intended to be used for audio manipulation.
    """

    # Audio formats that are currently supported.
    INPUT_AUDIO_FORMATS = ("mp3", "mpeg", "opus", "wav")
    OUTPUT_AUDIO_FORMATS = ("wav", "opus")

    def __init__(self) -> None:
        self.streams: Dict[str, AudioStream] = dict()
        self.default_input_audio_format = "wav"
        # Recording parameters
        self.recording_sample_rate = 44100
        self.recording_channels = 2
        self.recording_max_duration_seconds = 60 * 5
        self.recording_sample_width_bytes = 2

    def read_streams(self, file_paths: Dict[str, str]) -> bool:
        """
        Read the audio files at the given paths for future operations.
        If there is an error encountered while reading any single file,
        none of the files are read.
        Clears all previously read streams from memory.

        Args:
            file_paths (Dict[str,str]):
                Mapping from unique file name to its path.
        """
        # Clears all the previous streams when reading new ones.
        self.streams.clear()
        # Determine whether all files are valid
        if not all([self._is_audio_file(path) for path in file_paths.values()]):
            return False
         # If all files exist, they are read as AudioSegment objects.
        for name, file_path in file_paths.items():
            success, stream = self._initialize_audio_stream_from_file(
                file_path, self.default_input_audio_format, None, None)
            # Verify that the stream is successfully created.
            if not success:
                self.streams.clear()
                return False
            self.streams[name] = stream
        return True

    # TODO: This does not work properly. Needs to be fixed.
    def record_stream(self, identifier: str, duration_seconds: float) -> bool:
        """
        Record an audio stream with the given identifier and of
        duration_seconds.

        Args:
            identifier (str): identifier for the audio recording.
            duration_seconds (float): Recording duration.
        """
        if not 0 < duration_seconds <= self.recording_max_duration_seconds:
            return False
        try:
            recording = sd.rec(
                int(duration_seconds * self.recording_sample_rate),
                samplerate=self.recording_sample_rate,
                channels=self.recording_channels,
                blocking=True)
            # Load the array as an audio segment
            audio_segment = AudioSegment(
                data=recording.tobytes(),
                sample_width=2,
                frame_rate=self.recording_sample_rate,
                channels=self.recording_channels)
            self.streams.clear()
            success, stream = AudioSegment(
                "", self.default_input_audio_format, audio_segment, None, None)
            if success:
                self.streams[identifier] = stream
                return True
            return False
        except:
            return False

    def set_output_paths(self, output_dir_paths: Dict[str, str]) -> bool:
        """
        Set the output direcotry path for the audio streams associated with
        the identifiers.

        Args:
            output_dir_paths (Dict[str,str]):
                Mapping from identifier to output directory path.
                The path must be a valid directory path.
        """
        # Setting the output paths for each AudioStream
        for name, output_dir_path in output_dir_paths.items():
            # Verify identifiers and path
            if not name in self.streams or \
                    not self._is_directory(output_dir_path):
                return False
            self.streams[name].output_dir_path = output_dir_path
        return True

    def set_output_formats(self, output_formats: Dict[str, str]) -> bool:
        """
        Set the output formats for the audio streams associated with the
        identifiers.

        Args:
            output_formats (Dict[str,str]):
                Mapping from identifier to output format
                The format must be a supported output audio format.

        Returns:
            (bool): True if format successfully set. False otherwise.
       """
        # Setting the output paths for each AudioStream
        for name, output_format in output_formats.items():
            if not name in self.streams or \
                    not output_format in self.OUTPUT_AUDIO_FORMATS:
                return False
            self.streams[name].output_format = output_format
        return True

    ################################# GETTERS #############################

    def is_readable(self, file_path: str) -> bool:
        """
        Determine if the file at the given path is readable by AudioIO.
        """
        return self._is_audio_file(file_path)

    def get_stream_configurations(self) -> Dict[str, Dict[str, Any]]:
        """
        Obtain important configuration information for all files that have
        been read.

        Returns:
            (Dict[str,Dict[str,Any]]):
                Dictionary containing mappings from the unique  identifier /
                name of the file to a dictionary containing configuration
                information.
        """
        configs = dict()
        for name in self.streams.keys():
            audio_segment = self.streams[name].audio_segment
            configs[name] = {
                "decibels_relative_to_full_scale": audio_segment.dBFS,
                "channels": audio_segment.channels,
                "sample_width": audio_segment.sample_width,
                "frame_rate": audio_segment.frame_rate,
                "frame_width": audio_segment.frame_width,
                "root_mean_square": audio_segment.rms,
                "highest_amplitude": audio_segment.max,
                "duration_seconds": audio_segment.duration_seconds,
                "num_frames": audio_segment.frame_count()}
        return configs

    def get_stream_names(self) -> List[str]:
        """
        Get the unique identifiers / names of all the files that are currently
        ready to have operations performed on.

        Returns:
            (List[str]): Name of all files in stream.
        """
        return list(self.streams.keys())

    def get_streams(self) -> Dict[str, Any]:
        """
        Obtain all streams that have been read as byte arrays.

        Returns:
            (Dict[str,Any]): Mapping from file identifier / name to byte array.
        """
        streams = dict()
        for name in self.streams.keys():
            streams[name] = self.streams[name].audio_segment.raw_data
        return streams

    def get_supported_input_formats(self) -> List[str]:
        """
        Get the input audio file formats that are supported.
        """
        return list(self.INPUT_AUDIO_FORMATS)

    def get_supported_output_formats(self) -> List[str]:
        """
        Get the output audio file formats that are supported.
        """
        return list(self.OUTPUT_AUDIO_FORMATS)

    ############################### PUBLIC METHODS ########################

    def write(self, identifiers: List[str]) -> Tuple[bool, Dict]:
        """
        Write the audio stream associated with the given identifiers.
        If the output path and formats were not explicitly set, they default
        to the input directory path and input formats.

        Args:
            identifiers (List[str]): Unique identifiers for audio stream

        Returns:
            (bool): True if all files are successfully written. False otherwise.
        """
        paths = dict()
        # List to store success values
        is_success_list = list()
        # Verify all identifiers
        if not all([identifier in self.streams.keys()
                    for identifier in identifiers]):
            return False, paths
        # Write all the output files
        for name in identifiers:
            success, output_path = self._export_audio(
                self.streams[name].audio_segment,
                self.streams[name].output_dir_path,
                name,
                self.streams[name].output_format)
            is_success_list.append(success)
            paths[name] = output_path
        return all(is_success_list), paths

    def mono_to_stereo(self) -> Tuple[bool, str]:
        """
        Convert two mono streams into a single stereo stream.
        The streams must have the same number of frames.
        Only applies when there are only two streams that have been read.
        Previous streams will be discarded and only the stereo stream will be
        stored.

        Returns:
            (Tuple[bool,str]):
                True if successful. False otherwise.
                The string represents the unique identifier / name for the
                stereo stream.
        """
        # Ensure that we only have two streams to combine into stereo.
        if len(self.streams.keys()) != 2:
            return (False, None)
        # Obtain the audio segments
        name_1, name_2 = self.streams.keys()
        audio_segment_1 = self.streams[name_1].audio_segment
        audio_segment_2 = self.streams[name_2].audio_segment
        # Generate new file name and data for new stream.
        stereo_name = "{}_{}_stereo".format(name_1, name_2)
        output_dir_path = self.streams[name_1].output_dir_path
        output_format = self.streams[name_1].output_format
        # Attempt to combine into stereo.
        try:
            stereo_segment = AudioSegment.from_mono_audiosegments(
                audio_segment_1, audio_segment_2)
            stream = AudioStream(
                "", self.default_input_audio_format, stereo_segment,
                output_dir_path, output_format)
            # Clear existing streams is successful
            self.streams.clear()
            self.streams[stereo_name] = stream
            return (True, stereo_name)
        except:
            return (False, None)

    def stereo_to_mono(self) -> Tuple[bool, Tuple[str, str]]:
        """
        Convert a stereo stream to two mono streams i.e. left stream and right
        stream.
        Only applies when there is only one stereo stream that has been
        read.
        Afterwards, the stereo stream is deleted and the left and right
        streams are stored instead.

        Returns:
            (Tuple[bool, Tuple[str,str]]):
                True if successful. False otherwise.
                The Tuple represents the names /unique identifier of the left
                channel stream and the right channel stream.
        """
        # Only works when a single stereo audio file has been read.
        if len(self.streams.keys()) != 1:
            return (False, (None, None))
        # Generating names for channels
        name, = self.streams.keys()
        left_channel_name = name + "_left_channel_mono"
        right_channel_name = name + "_right_channel_mono"
        # Gathering data for new potential streams
        audio_segment = self.streams[name].audio_segment
        output_dir_path = self.streams[name].output_dir_path
        output_format = self.streams[name].output_format
        # Attempting to convert to mono.
        try:
            left_segment, right_segment = audio_segment.split_to_mono()
            self.streams.clear()
            # Creating streams for left and right channels.
            left_stream = AudioStream(
                "", self.default_input_audio_format, left_segment,
                output_dir_path, output_format)
            right_stream = AudioStream(
                "", self.default_input_audio_format, right_segment,
                output_dir_path, output_format)
            self.streams[left_channel_name] = left_stream
            self.streams[right_channel_name] = right_stream
            return (True, (left_channel_name, right_channel_name))
        except:
            return (False, (None, None))

    def concat(self) -> Tuple[bool, str]:
        """
        Combine all the streams into a single stream, one after another, in the
        specific order in which they were read. There must be at least one
        audio stream read before using this method.

        Returns:
            (Tuple[bool,str]):
                True + name of the combined stream if successful.
                False + "" otherwise.
        """
        # Do not do anything if no files have been read
        if len(self.streams.keys()) == 0:
            return (False, "")
        # Concat all existing segments
        combined_segment = AudioSegment.empty()
        for stream in self.streams.values():
            combined_segment += stream.audio_segment
        # Generate name
        combined_name = "_".join([name for name in self.streams.keys()])
        combined_name += "_concatenated"
        # Clear all existing streams
        self.streams.clear()
        # Store new stream
        self.streams[combined_name] = AudioStream(
            "", self.default_input_audio_format, combined_segment, None, None)
        return (True, combined_name)

    def overlay(self, loop_shorter_stream: bool = False) -> Tuple[bool, str]:
        """
        Overlays two audio streams on top of each other.
        Clears all existing streams and only stores the overlaid stream.

        Args:
            loop_shorter_stream (bool):
                If True, the shorter audio stream is looped i.e. starts playing
                again after it ends. If False, silence is inserted after the
                shorter audio stream until the longer stream finishes.
                False by default.

        Returns:
            (Tuple[bool,str]):
                True + name of the combined stream if successful.
                False + "" otherwise.
        """
        # Only two files can be overlayed
        if len(self.streams.keys()) != 2:
            return (False, "")
        # Determine the longer and shorted segments
        segment_1, segment_2 = [stream.audio_segment
                                for stream in self.streams.values()]
        if segment_1.duration_seconds < segment_2.duration_seconds:
            longer_segment, shorter_segment = segment_2, segment_1
        else:
            longer_segment, shorter_segment = segment_1, segment_2
        # Combine the segments
        if loop_shorter_stream:
            overlaid_segment = longer_segment.overlay(
                shorter_segment, loop=True)
        else:
            # Create a silent stream to cover duration difference
            duration_difference = longer_segment.duration_seconds - \
                shorter_segment.duration_seconds
            silence = AudioSegment.silent(duration=duration_difference)
            shorter_segment += silence
            overlaid_segment = longer_segment.overlay(shorter_segment)
        # Clear existing streams and store overlaid segment as new stream
        overlaid_name = "_".join(self.streams.keys())
        overlaid_name += "_overlaid"
        self.streams.clear()
        self.streams[overlaid_name] = AudioStream(
            "", self.default_input_audio_format, overlaid_segment, None, None)
        return (True, overlaid_name)

    def change_volume(self, change: Dict[str, int]) -> bool:
        """
        Change the volume of the given file names.

        Args:
            change (Dict[str,int]):
                Mapping from the name / unique identifier of the file to the
                amount that the volume has to be changed in decibels.
                Ex: 1 means no change, 2 means twice the volume, -2 means half
                the original volume etc.
        """
        # Ensure that the name is a stream that has been read.
        for name in change.keys():
            if name not in self.streams.keys():
                return False
        # Applying the gain
        for name, db_change in change.items():
            audio_segment = self.streams[name].audio_segment
            # Apply db change to the audio stream
            new_segment = audio_segment.apply_gain(db_change)
            self.streams[name].audio_segment = new_segment
        return True

    def reverse(self, names: List[str]) -> bool:
        """
        Reverse the audio stream with the name / identifier.

        Args:
            names (List[str]): Names of the streams to reverse. Must have
                            been read before using this method.
        """
        # Ensure name is present / has been read.
        for name in names:
            if name not in self.streams.keys():
                return False
        # Reverse the appropriate streams
        for name in names:
            audio_segment = self.streams[name].audio_segment
            reversed_segment = audio_segment.reverse()
            self.streams[name].audio_segment = reversed_segment
        return True

    def chunk(self, chunks: Dict[str, int]) \
            -> Tuple[bool, Dict[str, List[str]]]:
        """
        Chunks the streams with the given names / unique identifiers into
        segments of the defined duration. If the duration of the chunk is
        greater than the duration of the stream, it is not changed.
        The original stream is deleted.
        NOTE: The duration of the chunks is in seconds.

        Args:
            chunks (Dict[str,int]):
                Mapping from name / identifier of stream to the duration of
                each chunk in seconds.
                The duration has to be a positive value.

        Returns:
            (Tuple[bool, Dict[str,List[str]]]):
                True if successful. False otherwise.
                The dictionary is a mapping from the name of stream to a list
                containing the names of streams the original stream is chunked
                into.
        """
        # All the names should be already read stream names.
        # The chunk durations should be valid
        for name, chunk_duration_seconds in chunks.items():
            if name not in self.streams.keys() or \
                    chunk_duration_seconds <= 0:
                return (False, {})
        # Mappings to store the new stream names and their relationships with
        # original stream.
        try:
            name_mappings = dict()
            new_streams = dict()
            for name, chunk_duration_seconds in chunks.items():
                audio_segment = self.streams[name].audio_segment
                # Chunk based on the duration given.
                if audio_segment.duration_seconds <= chunk_duration_seconds:
                    name_mappings[name] = [name]
                    new_streams[name] = deepcopy(self.streams[name])
                else:
                    chunk_names = list()
                    duration_ms = chunk_duration_seconds * 1000
                    for i, chunk_segment in enumerate(audio_segment[::duration_ms]):
                        chunk_name = "{}_chunk_{}".format(name, i)
                        new_streams[chunk_name] = AudioStream(
                            "", self.default_input_audio_format, chunk_segment, None,
                            "wav")
                        chunk_names.append(chunk_name)
                    name_mappings[name] = chunk_names
            self.streams.clear()
            self.streams = new_streams
            return (True, name_mappings)
        except Exception as e:
            print(e)

    # -------------------------- PRIVATE METHODS

    def _export_audio(
            self, audio_segment: AudioSegment,
        output_dir_path: str, name: str, output_format: str) \
            -> Tuple[bool, str]:
        """
        Export the audio stream.

        Args:
            audio_segment (AudioSegment): Segment to export.
            output_dir_path (str): Directory path for the output file.
                                Must be a valid directory path.
            name (str): File name. Does not include extension.
            output_format (str): Format of the output file.
                            Must be a supported output format.
        """
        try:
            if not self._is_directory(output_dir_path) or \
                    not output_format in self.OUTPUT_AUDIO_FORMATS:
                return False, None

            output_file_path = "{}/{}.{}".format(
                output_dir_path, name, output_format)
            audio_segment.export(output_file_path, format=output_format)
            return True, output_file_path
        except Exception as e:
            return False, None

    def _initialize_audio_stream_from_file(
            self, input_file_path, input_format,
            output_dir_path, output_format) -> AudioStream:
        """
        Initializes and returns an AudioStream object by reading from input path.
        """
        try:
            audio_segment = AudioSegment.from_file(input_file_path,
                                                   format=input_format)
            # Output format defaults to the input format if not specified.
            if output_format == None:
                output_format = input_format
            # The output path defaults to the input path directory if not specified
            if len(input_file_path) > 0 and \
                    output_dir_path == None and \
                    input_file_path.find("/") != -1:
                output_dir_path = input_file_path[:input_file_path.rfind("/")]
            stream = AudioStream(
                input_file_path, input_format, audio_segment, output_dir_path,
                output_format)
            return (True, stream)

        except:
            return (False, None)

    def _does_file_exist(self, file_path: str) -> bool:
        """
        Determines if the file exists.
        """
        return os.path.exists(file_path) and os.path.isfile(file_path)

    def _is_audio_file(self, file_path: str) -> bool:
        """
        Determine if the file exists and is of a supported audio file format.
        """
        return self._does_file_exist(file_path) and \
            self._get_file_extension(file_path).lower() in \
            self.INPUT_AUDIO_FORMATS

    def _is_directory(self, dir_path: str) -> bool:
        """
        Determine if path is a directory.
        """
        return os.path.isdir(dir_path)

    def _get_file_extension(self, file_path: str) -> str:
        """
        Obtain file extension /format, which is the substring after the right-
        most "." character.
        """
        return os.path.splitext(file_path.strip())[1][1:]
