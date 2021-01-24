# Standard library imports 
import os
from typing import Dict, List, Any, Tuple
# Local imports 

# Third party imports 
from pydub import AudioSegment
from copy import deepcopy

class AudioIO:
    """
    Provides methods that directly interact with and can modify audio streams 
    and files. Intended to be used for audio manipulation.
    """

    # Audio formats that are currently supported.
    AUDIO_FORMATS = ("alaw", "basic", "flaf", "g729", "pcm", "mp3", "mpeg", 
                    "ulaw", "opus", "wav", "webm")

    def __init__(self) -> None:
        """
        Params:
            streams (Dict[str, Dict[str,AudioSegment]]]): 
                Mapping of the unique identifier / name of an audio stream 
                to a dictionary containing: 
                    1. Path of the file.
                    2. AudioSegment object associated with that file.
            
        """
        self.streams = dict() 
        # TODO: Write documentation for this.
        self.default_audio_format = "wav"

    ################################# SETTERS ###############################
    def read_streams(self, file_paths : Dict[str,str]) -> bool:
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
        # If all files exist, they are read as AudioSegment objects. 
        for name, file_path in file_paths.items():
            if not self._is_audio_file(file_path):
                self.streams.clear()
                return False 
            self.streams[name] = {
                "file_path" : file_path,
                "audio_segment" : AudioSegment.from_file(
                    file_path,format=self.default_audio_format)}
        return True
   

    ################################# GETTERS #############################
    def get_stream_configurations(self) -> Dict[str,Dict]:
        """
        Obtain important configuration information for all files that have 
        been read.

        Returns:
            (Dict[str,Dict]): 
                Dictionary containing mappings from the unique  identifier / 
                name of the file to a dictionary containing configuration 
                information.
                Configuration information includes:
                    1. decibels_relative_to_full_scale
                    2. channels
                    3. sample width
                    4. frame rate 
                    5. frame width
                    6. rms
                    7. highest amplitude
                    8. duration in seconds
                    9. number of frames.
        """
        configs = dict()
        for name in self.streams.keys():
            audio_segment = self.streams[name]["audio_segment"]
            configs[name] = {
                "decibels_relative_to_full_scale" : audio_segment.dBFS,
                "channels" : audio_segment.channels,
                "sample_width" : audio_segment.sample_width,
                "frame_rate" : audio_segment.frame_rate, 
                "frame_width" : audio_segment.frame_width,
                "root_mean_square" : audio_segment.rms,
                "highest_amplitude" : audio_segment.max, 
                "duration_seconds" : audio_segment.duration_seconds, 
                "num_frames" : audio_segment.frame_count()}
        return configs
    
    def get_stream_names(self) -> List:
        """
        Get the unique identifiers / names of all the files that are currently 
        ready to have operations performed on.

        Returns:
            (List): Name of all files in stream.
        """
        return list(self.streams.keys()) 

    def get_streams(self) -> Dict[str,Any]:
        """
        Obtain all streams that have been read as byte arrays.

        Returns:
            (Dict[str,Any]): Mapping from file identifier / name to byte array.
        """
        streams = dict()
        for name in self.streams.keys():
            audio_segment = self.streams[name]["audio_segment"]
            streams[name] = audio_segment.raw_data
        return streams

    def get_supported_formats(self) -> Tuple:
        """
        Get the audio file formats that are supported.

        Returns:
            (Tuple): Supported audio file formats
        """
        return tuple(self.AUDIO_FORMATS)

    ############################### PUBLIC METHODS ########################

    def write(self, output_paths : Dict[str,str]) -> bool:
        """
        Write streams that were previously read. 

        Args:
            output_paths ( Dict[str,str]):
                Mapping from stream identifier / name to output paths.
        
        Returns:
            (bool): True if successful. False otherwise.
        """
        # Verify that all the given output paths have streams associated.
        # and that the output paths are directories.
    
        for name in output_paths.keys():
            if not name in self.streams.keys() or \
                not self._is_directory(output_paths[name]):
                    return False 
            # If stream exists and path is a directory, then export.
            audio_segment = self.streams[name]["audio_segment"]
            output_file_name = "{}/{}.{}".format(
                output_paths[name],name,self.default_audio_format)
            audio_segment.export(
                output_file_name, self.default_audio_format)
        return True


    def mono_to_stereo(self) -> Tuple[bool,str]:
        """
        Convert two mono streams into a single stereo stream. The streams must
        have the same number of frames. Only applies when there are only 
        two streams that have been read. AudioIO will only contain the stereo 
        stream if operation is successful.The original streams will be removed.
        The combined file has the name: [identifier-1]_[identifier-2].

        Returns:
            (Tuple[bool,str]): 
                True if successful. False otherwise.
                The string represents the unique identifier / name for the 
                stereo stream.
        """
        # Ensure that we only have two streams to combine into stereo. 
        if len(self.streams.keys()) != 2:
            return (False, "")
        # Ensure that the two files have the same frame count.
        name_1,name_2 = self.streams.keys()
        audio_segment_1 = self.streams[name_1]["audio_segment"]
        audio_segment_2 = self.streams[name_2]["audio_segment"]
        stereo_name = "{}_{}".format(name_1,name_2)
        try:
            stereo_stream = AudioSegment.from_mono_audiosegments(
                audio_segment_1,audio_segment_2)
            self.streams.clear()
            self.streams[stereo_name] = {
                "file_path" : "", 
                "audio_segment" : stereo_stream}
            return (True ,stereo_name)
        except:
            return (False,"")

    def stereo_to_mono(self) -> Tuple[bool, Tuple[str,str]]:
        """
        Convert a stereo stream to two mono streams i.e. left stream and right 
        stream. Only applies when there is only one stereo stream that has been
        read. Afterwards, the stereo stream is deleted and the left and right 
        streams are stored instead.

        Returns:
            (Tuple[bool, Tuple[str,str]]):
                True if successful. False otherwise.
                The Tuple represents the names /unique identifier of the left 
                channel stream and the right channel stream.
        """
        # Only works when a single stereo audio file has been read.
        if len(self.streams.keys()) != 1:
            return (False, ())
        name, = self.streams.keys()
        left_channel_name = name + "left_channel"
        right_channel_name = name + "right_channel"
        audio_segment = self.streams[name]["audio_segment"]
        try:
            left_channel, right_channel = audio_segment.split_to_mono()
            self.streams.clear()
            self.streams[left_channel_name] = {
                "file_path" : "",
                "audio_segment" : left_channel}
            self.streams[right_channel_name] = {
                "file_path" : "",
                "audio_segment" : right_channel}
            return (True, (left_channel_name,right_channel_name))
        except:
            return (False, ()) 
    
    def concat(self) -> Tuple[bool,str]:
        """
        Combine all the streams into a single stream, one after another, in the 
        specific order in which they were read. There must be at least one 
        audio stream read before using this method.

        Returns:
            (Tuple[bool,str]):
                True + name of the combined stream if successful.
                False + "" otherwise.
        """
        # Do not do anything if there are no files read 
        if len(self.streams.keys()) == 0:
            return (False, "")
        combined_stream = AudioSegment.empty()
        for stream in self.streams.values():
            audio_segment = stream["audio_segment"]
            combined_stream += audio_segment 
        # Clear all existing streams 
        combined_name = "_".join([name for name in self.streams.keys()])
        self.streams.clear()
        # Storing new concatenated stream.
        self.streams[combined_name] = {
                "file_path" : "",
                "audio_segment" : combined_stream}
        return (True, combined_name)

    def overlay(self, loop_shorter_stream : bool = False) -> Tuple[bool,str]:
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
        # Determine the shorter segment.
        segment_1, segment_2 = [stream["audio_segment"] for \
            stream in self.streams.values()]
        # Determining which the initial and ending streams are.
        if segment_1.duration_seconds < segment_2.duration_seconds:
            longer_stream = segment_2 
            shorter_stream = segment_1 
        else:
            longer_stream = segment_1
            shorter_stream = segment_2
        # Combine the streams
        if loop_shorter_stream:
            overlaid_stream = longer_stream.overlay(shorter_stream,loop=True)
        else:
            # Determine the duration difference and create a silent stream 
            duration = longer_stream.duration_seconds - \
                shorter_stream.duration_seconds 
            silence = AudioSegment.silent(duration = duration)
            shorter_stream += silence 
            overlaid_stream = longer_stream.overlay(shorter_stream)
        # Clear other streams and store the overlaid streams 
        overlaid_name = "_".join(self.streams.keys())
        self.streams.clear()
        self.streams[overlaid_name] = {
                "file_path" : "",
                "audio_segment" : overlaid_stream}
        return (True, overlaid_name)

    def change_volume(self, change : Dict[str, int]) -> bool:
        """
        Change the volume of the given file names.

        Args:
            change (Dict[str,int]):
                Mapping from the name / unique identifier of the file to the 
                amount that the volume has to be changed in decibels.
                Ex: 1 means no change, 2 means twice the volume, -2 means half
                the original volume etc.
        
        Returns:
            (bool): True if successful. False otherwise.
        """
        # Ensure that the name is a stream that has been read.
        for name in change.keys():
            if name not in self.streams.keys():
                return False 
        # Applying the gain
        for name, db_change in change.items():
            audio_segment = self.streams[name]["audio_segment"]
            # Apply db change to the audio stream 
            new_segment = audio_segment.apply_gain(db_change)
            self.streams[name]["audio_segment"] = new_segment
        return True 

    def reverse(self, names : List[str]) -> bool:
        """
        Reverse the audio stream with the name / identifier.

        Args:
            names (List[str]): Names of the streams to reverse. Must have 
                            been read before using this method.

        Returns:
            (bool): True if successful. False otherwise.
        """
        # Ensure name is present / has been read.
        for name in names:
            if name not in self.streams.keys():
                return False 
        # Reverse the appropriate streams
        for name in names:
            audio_segment = self.streams[name]["audio_segment"]
            reversed_segment = audio_segment.reverse()
            self.streams[name]["audio_segment"] = reversed_segment 
        return True 

    def chunk(self, chunks : Dict[str, int]) -> Tuple[bool, Dict[str,List[str]]]:
        """
        Chunks the streams with the given names / unique identifiers into 
        segments of the defined duration. If the duration of the chunk is 
        greater than the duration of the stream, it is not changed.
        The original stream is deleted.
        NOTE: The duration of the chunks is in seconds.

        Args:
            chunks (Dict[str,name]):
                Mapping from name / identifier of stream to the duration of each 
                chunk. 
                The duration has to be a positive value.

        Returns:
            (Tuple[bool, Dict[str,List[str]]]): 
                True if successful. False otherwise.
                The dictionary is a mapping from the name of stream to a list 
                containing the names of streams the original stream is chunked 
                into.
        """
        # All the names should be already read stream names.
        for name in chunks.keys():
            if name not in self.streams.keys():
                return (False, {})
        new_streams = dict()
        name_mappings = dict()
        # Otherwise, we need to chunk into given durations 
        for name, chunk_duration_seconds in chunks.items():
            # Ensure that the chunk duration is valid and positive.
            if chunk_duration_seconds <= 0:
                return (False, {})
            # Determine original audio length
            audio_segment = self.streams[name]["audio_segment"]
            name_mappings[name] = list()
            # Do not chunk if chunk duration is greater
            if audio_segment.duration_seconds <= chunk_duration_seconds:
                name_mappings[name].append([name])
                new_streams[name] = deepcopy(self.streams[name])
            else:
                chunk_names = list()
                duration_ms = chunk_duration_seconds * 1000
                for i, chunk in enumerate(audio_segment[::duration_ms]):
                    chunk_name = "{}_chunk_{}".format(name, i)
                    new_streams[chunk_name] = {
                    "file_path" : "",
                    "audio_segment" : chunk}
                    chunk_names.append(chunk_name)
                name_mappings[name].append(chunk_names)
        self.streams.clear()
        self.streams = new_streams
        return (True, name_mappings)

    ############################# PRIVATE METHODS ##########################
    
    ### Others 

    def _does_file_exist(self, file_path : str) -> bool:
        """
        Determines if the file exists.

        Args:
            file_path (str)
        
        Returns:
            (bool): True if file exists. False otherwise.
        """
        return os.path.exists(file_path) and os.path.isfile(file_path)

    def _is_audio_file(self, file_path : str) -> bool:
        """
        Determine if the file exists and is of a supported audio file format.

        Args:
            file_path (str)

        Returns:
            (bool): True if file exists and is audio file. False otherwise.
        """
        return self._does_file_exist(file_path) and \
            self._get_file_extension(file_path).lower() in self.AUDIO_FORMATS

    def _is_directory(self, dir_path : str) -> bool:
        """
        Determine if path is a directory.

        Args:
            (str): Path 
        
        Returns:
            (bool): True if path is a directory. False otherwise.
        """
        return os.path.isdir(dir_path)
    
    def _get_file_extension(self, file_path : str) -> str:
        """
        Obtain file extension /format, which is the substring after the right-
        most "." character.

        Args:
            file_path (str)
        
        Returns:
            (str): File extension / format.
        """
        return os.path.splitext(file_path.strip())[1][1:]