# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 16:28:17
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-16 14:33:08

from typing import List, Union, Dict
import os
from dataclasses import dataclass
from abc import ABC 
from .general import (
    get_extension,
    get_name,
    make_dir, 
    run_cmd,
    get_cmd_status,
    is_directory, 
    paths_in_dir,
    CMD_STATUS
)
from gailbot.core.utils.logger import makelogger 
from pydub import AudioSegment
from pydub.silence import detect_leading_silence
MERGED_FILE_NAME = "merged"
logger = makelogger("media")
@dataclass
class Stream(ABC):
    """ Abstract class that defines the representation of a media stream 
    
    Attributes
    name : str
        the name of the stream file 
    source : Union [List[str], List[Stream]]
        the source of the stream, which can either be a list of paths to a media 
        file or a list of media Stream  
    extension : str
        the file extension, which tells the file type 
    """
    source : Union[List[str], List["Stream"]]
    name : str
    extension : str

@dataclass
class AudioStream(Stream):
    """ A subclass of Steam class which defines the representation of 
        audio stream 
    
    Attributes
    segment : AudioSegment
        stores source of an audio segment 
        
    """
    segment : AudioSegment

    def __repr__(self):
        print(f"audio stream {self.name}\n")

@dataclass
class VideoStream(Stream):
    """ A subclass of Steam class which defines the representation of 
        Video stream 
    
    """
    pass

    def __repr__(self):
        return f"video stream {self.name}\n"

class AudioHandler:
    """ Implement a class that contains functions to handle audio file 

    Attributes
        _SUPPORTED_FORMATS: List[str]
            a list of supported audio format
        _DEFAULT_FORMAT: 
            the default audio format         
    """

    _SUPPORTED_FORMATS = ["mp3", "mpeg", "opus", "wav"]
    _DEFAULT_FORMAT = "wav"


    def __repr__(self) -> str:
        return "Audio Stream handler"
    
    @property
    def supported_formats(self) -> List[str]:
        """ return a list of string with supported audio format"""
        return self._SUPPORTED_FORMATS

    @staticmethod    
    def is_supported(path : str) -> bool:
        """ tell if a audio file is supported by the AudioHandler

        Args:
            path (str): a path to a file

        Returns:
            bool: return true of the file is supported 
        """
        return get_extension(path) in ["mp3", "mpeg", "opus", "wav"]
        
    def read_file(self,path : str) -> AudioStream:
        """ read the audio file data

        Args:
            path (str): a path to a file 

        Returns:
            AudioStream: return the audio file data as an AudioStream object 
                         if the file type is supported, return nothing 
                         if the file type is unsupported  
        """
        if not AudioHandler.is_supported(path):
            return
        format = get_extension(path)
        segment = AudioSegment.from_file(
            path, format=format
        )
        return AudioStream(
            source=[path],
            name=get_name(path),
            extension=format,
            segment=segment
        )

    def record(
        self,
        name : str,
        out_dir : str,
        duration_sec : float = -1,
    ) -> AudioStream:
        """ record the audio file 
        """
        raise NotImplementedError()

    def write_stream(
        self,
        stream : AudioStream,
        outdir : str,
        name : str = None,
        format : str = None
    ) -> str:
        """ write a stream with the given format. If not format or name is 
            specified, uses the stream's default name and format.
        
        Args: 
            stream: AudioStream 
                stores the audio file data as an instance of AudioStream 
            outdir: str 
                a path that stores the output directory 
            name: str (Optional)
                file name, default to the name of stream 
            format: str (Optional)
                file format, default to the extension of  stream 
        
        Return:
            the file path 
        """
        if format not in self.supported_formats:
            raise Exception(f"Format {format} not supported")
        # Construct output file path
        name = stream.name if name == None else name
        ext = stream.extension if format == None else format
        make_dir(outdir,overwrite=False)
        path = f"{outdir}/{name}.{ext}"
        stream.segment.export(path,format=ext)
        return path

    def info(self, stream : AudioStream) -> Dict:
        """Get information about the given audio stream
        
        Args: 
            stream: AudioStream 
                stores the audio file data as an instance of AudioStream 
        
        Return:
            a dictionary with the stream information 
        """
        segment = stream.segment
        return {
                "name" : stream.name,
                "format" : stream.extension,
                "source" : stream.source,
                "decibels_relative_to_full_scale": segment.dBFS,
                "channels": segment.channels,
                "sample_width": segment.sample_width,
                "frame_rate": segment.frame_rate,
                "frame_width": segment.frame_width,
                "root_mean_square": segment.rms,
                "highest_amplitude": segment.max,
                "duration_seconds": segment.duration_seconds,
                "num_frames": segment.frame_count(),
        }

    def change_volume(
        self,
        stream : AudioStream,
        change_db : float
    ) -> AudioStream:
        """
        Apply the specified gain to the audio stream.
        Args:
            stream: AudioStream 
                stores the audio file data as an instance of AudioStream 
            change_db: float 
                the targeting value of the volume
        
        Return: 
            the resulting audio stream as an instance of AudioStream
        """
        segment = stream.segment.apply_gain(change_db)
        stream.segment = segment
        return stream

    def mono_to_stereo(
        self,
        left_stream : AudioStream,
        right_stream : AudioStream
    ) -> AudioStream:
        """
        Get a new stereo stream from the two mono streams
        Args: 
            left_stream: AudioStream
                stores the data of a mono audio file
            right_stream: AudioStream
                stores the data of a mono audio file 
        
        Return:
            the resulting audio stream as an instance of AudioStream
        """
        stereo_name = f"{left_stream.name}_{right_stream.name}_stereo"
        sources = [left_stream,right_stream]
        segment = AudioSegment.from_mono_audiosegments(
            left_stream.segment,right_stream.segment
        )
        return AudioStream(
            sources, stereo_name,self._DEFAULT_FORMAT,segment
        )
    
    def stereo_to_mono(
        self,
        stream : AudioStream
    ) -> List[AudioStream]:
        """
        Convert the given stereo stream to mono.
        
        Args: 
            stream: AudioStream 
                stores the data of a stereo audio file 
        
        Returns:
            a list of two mono audio file 
            
        """

        left_segment, right_segment = stream.segment.split_to_mono()
        left_stream = AudioStream(
            [stream],f"{stream.name}_left",self._DEFAULT_FORMAT,left_segment
        )
        right_stream = AudioStream(
            [stream],f"{stream.name}_right", self._DEFAULT_FORMAT,right_segment
        )
        return left_stream, right_stream

    def concat(self, streams : List[AudioStream]) -> AudioStream:
        """
        Concat the given stream end to end, start to finish, into a single stream.
        
        Args: 
            streams: List[AudioStream]
                A list of audio streams 
        
        Returns: 
            the resulting audio stream that is composed by concatenating the 
            input streams 
        """
        concatenated = AudioSegment.empty()
        for stream in streams:
            concatenated += stream.segment
        name = "_".join([stream.name for stream in streams])
        name += "_concatenated"
        return AudioStream(
            source=[streams],
            name=name,
            extension=self._DEFAULT_FORMAT,
            segment=concatenated
        )

    def overlay(
        self,
        left_stream : AudioStream,
        right_stream : AudioStream,
        loop_shorter_stream : bool = False
    ) -> AudioStream:
        """
        Overlay two audio streams on top of each other
        
        Args: 
            left_stream:AudioStream
                stores one audio file data that will be overlayed 
            right_stream:AudioStream
                stores one audio file data that will be overlayed 
            loop_shorter_stream: bool
                if true, the shorter audio file will be looped until it reaches
                the length of the longer audio file 
        """
        # Determine which segment is longer
        if left_stream.segment.duration_seconds > right_stream.segment.duration_seconds:
            segments = [left_stream.segment, right_stream.segment]
        else:
            segments = [right_stream.segment,left_stream.segment]
        if loop_shorter_stream:
            overlaid_segment = segments[0].overlay(segments[1], loop=True)
        else:
            # Create a silent stream to cover duration difference
            duration_diff = segments[0].duration_seconds - segments[1].duration_seconds
            silence = AudioSegment.silent(duration=duration_diff)
            segments[1] += silence
            overlaid_segment = segments[0].overlay(segments[1])
        name = f"{left_stream.name}_{right_stream.name}_overlaid"
        return AudioStream(
            [left_stream,right_stream], name, self._DEFAULT_FORMAT,
            overlaid_segment
        )

    
    
    def reverse(self, stream : AudioStream) -> AudioStream:
        """
        Reverse the given audio stream 
        
        Args:
            stream: AudioStream
                stores the data of an audio stream
        Returns:
            the resulting audio stream after reversed
        """
        reversed_segment = stream.segment.reverse()
        stream.segment = reversed_segment
        return stream

    def chunk(
        self,
        stream : AudioStream,
        chunk_duration_s : float
    ) -> List[AudioStream]:
        """
        Generate chunks of the given audio with the provided duration.
        
        Args: 
        stream: AudioStream
                stores the data of an audio stream
        
        Returns:
            a list of audio stream, which are the chunks of the given audio 
            stream

        """
        assert chunk_duration_s > 0, f"Duration must be positive"
        # Simply return original stream if no chunking possible.
        if chunk_duration_s > stream.segment.duration_seconds:
            return [stream]

        duration_ms = chunk_duration_s * 1000
        chunks = list()
        for i, chunk_segment in enumerate(stream.segment[::int(duration_ms)]):
            name = f"{stream.name}_{chunk_duration_s}_chunk_{i}"
            chunk = AudioStream(
                [stream],name, self._DEFAULT_FORMAT,chunk_segment
            )
            chunks.append(chunk)
        return chunks

    @staticmethod
    def convert_to_16bit_wav(input_path, output_path):
        pid = run_cmd(["ffmpeg", "-i", input_path, "-acodec", "pcm_s16le", "-ar", "16000", output_path])
        while True:
            match get_cmd_status(pid):
                case CMD_STATUS.STOPPED:
                    logger.error("process was stopped when converting the audio file to 16bit_wav format")
                    break
                case CMD_STATUS.FINISHED:
                    return output_path
                case CMD_STATUS.ERROR:
                    logger.error("error in converting the audio file to 16bit_wav format")
                    break
                case CMD_STATUS.NOTFOUND:
                    break
        logger.warn("cannot convert the file to 16bit_wav file format, use original file instead")
        return input_path
    
    @staticmethod 
    def compress_to_opus(audio_path:str, output_dir:str):
        """ compress the audio file stored in audio_path to output_dir, 
            with the same audio file name with opus format

        Args:
            audio_path (str): the path to original file 
            output_dir (str): the path to the directory where the compressed file 
                              will be stored

        Raises:
            ChildProcessError: 
            ChildProcessError: 
            ProcessLookupError: 

        Returns:
            str: the path to the compressed file
        """
        logger.info("Converting file")
        out_path = "{}/{}.opus".format(output_dir, get_name(audio_path))
        logger.info(f"Converting path{out_path}")
        pid = run_cmd(["ffmpeg", "-y", "-i", audio_path, "-strict", "-2", out_path])
        
        while True:
            match get_cmd_status(pid):
                case CMD_STATUS.STOPPED:
                    raise ChildProcessError("ERROR: child process error")
                case CMD_STATUS.FINISHED:
                    break 
                case CMD_STATUS.ERROR:
                    raise ChildProcessError("ERROR: child process error")
                case CMD_STATUS.NOTFOUND:
                    raise ProcessLookupError("ERROR: process lookup error")
        
        if get_cmd_status(pid) == CMD_STATUS.FINISHED:
            return out_path
        else: 
            return False
    
    @staticmethod 
    def chunk_audio_to_outpath(audio_path:str, output_path:str, chunk_duration:int) -> List[str]:
        """ given the audio path, chunking the audio into a series of audio
            segment
        
        Args:
            audio_path[str]: the file path to the audio file 
            output_path[str]: the output of the chunked file 
            duration[int]: the length of each chunk
            
        Return:
            Union[List[str], bool]: return a list of the audio path to the 
                                    chunked audios in order 
        """
        if not is_directory(output_path):
            make_dir(audio_path)
        basename = get_name(audio_path)
        dir = os.path.join(output_path, f"{basename}_audio_chunks")
        make_dir(dir)
        idx = 0
        try:
            mediaHandler = MediaHandler()
            stream = mediaHandler.read_file(audio_path)
            chunks = mediaHandler.chunk(stream, chunk_duration)
            for chunk in chunks:
                mediaHandler.write_stream(
                    chunk, dir, name=f"{basename}-{idx}", 
                    format=get_extension(audio_path))
                idx += 1
                
            audio_chunks = paths_in_dir(dir)
            audio_chunks = sorted(audio_chunks, key=lambda file: (len(file), file))
            
        except Exception as e:
            logger.error(e, exc_info=e)
        else:
            
            return audio_chunks


    def overlay_audios(self, audios: List[str], output_path: str, name = MERGED_FILE_NAME):
        res = self.read_file(audios[0])
        name = MERGED_FILE_NAME
        if len(audios) == 1:
            res = self.read_file(audios[0])
        else:
            for i in range(1, len(audios)):
                if AudioHandler.is_supported(audios[i]):
                    nxt = self.read_file(audios[i])
                    res = self.overlay(res, nxt)
        return self.write_stream(res, output_path, name=name, format=get_extension(audios[0]))


class VideoHandler:

    _SUPPORTED_FORMATS = ["mxf"]
    _BASE_FORMAT = "mp4"

    @property
    def supported_formats(self) -> List[str]:
        return self._SUPPORTED_FORMATS


    @staticmethod
    def is_supported(path : str) -> bool:
        return get_extension(path) in ["mxf"]


    def read_file(self, path : str) -> VideoStream:
        raise NotImplementedError()

    def record(
        self,
        name : str,
        out_dir : str,
        duration_sec : float = -1,
    ) -> VideoStream:
        raise NotImplementedError()

    def write_stream(
        self,
        stream : VideoStream,
        out_dir : str,
        name : str = None,
        extension : str = None
    ) -> str:
        raise NotImplementedError()

    def info(self, stream : VideoStream) -> Dict:
        raise NotImplementedError()

    def change_volume(
        self,
        stream : VideoStream,
        change_db : float
    ) -> VideoStream:
        raise NotImplementedError()

    def extract_audio(self, stream : VideoStream) -> AudioStream:
        raise NotImplementedError()

    def remove_audio(self, stream : VideoStream) -> VideoStream:
        raise NotImplementedError()

class MediaHandler:
    def __init__(self):
        """
        Initializes an object of the MediaHandler class, an abstraction of the AudioHandler and 
        VideoHandler classes.
        """
        self.audio_h = AudioHandler()
        self.video_h = VideoHandler()
        self._SUPPORTED_FORMATS = self.audio_h.supported_formats + self.video_h.supported_formats
    
    def __repr__(self) -> str:
        return "Media Stream Handler"
    
    
    @property
    def supported_formats(self) -> List[str]:
        """ 
        Accesses list of supported formats.

        Args:
            Self
        Returns:
            A list of strings representing supported formats of the given MediaHandler object
        """
        return self._SUPPORTED_FORMATS

    #### Audio and Video
    @staticmethod
    def is_supported(path: str) -> bool:
        return AudioHandler.is_supported(path) or \
               VideoHandler.is_supported(path)


    @staticmethod
    def is_audio(path : str) -> bool:
        """
        Determines if the given file is an audio file.
        
        Args:
            path: Path to given file in string form
        
        Returns:
            True if the given file is an audio file, false if the given file 
            is not an audio file.
        """
        return AudioHandler.is_supported(path)

    @staticmethod
    def is_video(path : str) -> bool:
        """
        Determines if the given file is a video file.

        Args:
            path: Path to given file in string form
        
        Returns:
            True if the given file is a video file, false if the given file 
            is not a video file.
        """
        return VideoHandler.is_supported(path)


    def read_file(self, path : str) -> Stream:
        """
        Reads inputted file.

        Args:
            path: Path to given file in string form

        Returns:
            An AudioStream or VideoStream containing the read stream.
            Raises exception if path is not supported.

        """
        if get_extension(path) in self.audio_h.supported_formats:
            return self.audio_h.read_file(path)
        elif get_extension(path) in self.video_h.supported_formats:
            return self.video_h.read_file(path)
        else:
            raise Exception(
                f"ERROR: Format not supported for file: {path}"
            )

    def record(
        self,
        name : str,
        out_dir : str,
        out_stream_type : Union[AudioStream, VideoStream],
        duration_sec : float = -1,
    ) -> Stream:
        """
        Records audio or video file from inputted stream.

        Args:
            name: File name as a string.
            out_dir: Path of the desired output directory as a string.
            out_stream_type: AudioStream or VideoStream, depending on the inputted file.
            duration_sec: Float containing the duration to record.

        Returns:
            Currently will raise NotImplementedError.
        """
        if out_stream_type == AudioStream:
            return self.audio_h.record(name, out_dir, duration_sec)
        else:
            return self.video_h.record(name, out_dir, duration_sec)


    def write_stream(
        self,
        stream : Stream,
        out_dir : str,
        name : str = None,
        format : str = None
    ) -> str:
        """
        Writes audio or video stream to given output directory.

        Args:
            stream: Inputted stream, of type AudioStream or VideoStream.
            out_dir: Path of the desired output directory as a string.
            name: File name as a string.
            format: Audio format as a string.

        Returns:
            Output as type stream.
        """
        return self._get_handler(stream).write_stream(
            stream, out_dir, name, format
        )

    def info(self, stream : Stream) -> Dict:
        """
        Accesss audio or video information

        Args:
            stream: Inputted stream, of type AudioStream or VideoStream.

        Returns:
            Information pertaining to the inputted stream in the form of a dictionary 
            with different data fields.
        """
        return self._get_handler(stream).info(stream)

    def change_volume(
        self,
        stream : Stream,
        change_db : float
    ) -> Stream:
        """
        Change audio or video information by given scale
        
        Args:
            stream: Inputted stream, of type AudioStream or VideoStream.
            change_db: Float value representing the decibals by which to change the volume.
            
        Returns:
            The resulting stream as an instance of AudioStream or VideoStream.
           """
        return self._get_handler(stream).change_volume(stream, change_db)

    ### Audio Methods
    def mono_to_stereo(
        self,
        left_stream : AudioStream,
        right_stream : AudioStream
    ) -> AudioStream:
        """
        Converts the given mono stream to stereo.

         Args: 
            left_stream: AudioStream
                stores the data of a mono audio file
            right_stream: AudioStream
                stores the data of a mono audio file 
        
        Returns:
            the resulting stereo audio stream as an instance of AudioStream.

        """
        return self.audio_h.mono_to_stereo(left_stream, right_stream)

    def stereo_to_mono(
        self,
        stream : AudioStream
    ) -> List[AudioStream]:
        """
        Converts the given stereo stream to mono.

        Args: 
            stream: AudioStream 
                stores the data of a stereo audio file 
        
        Returns:
            a list of two mono audio streams representing the two files.
        """
        return self.audio_h.stereo_to_mono(stream)

    def concat(self, streams : List[AudioStream]) -> AudioStream:
        """
        Concatenates the given stream end to end, start to finish, into a single stream.

        Args:
            streams: List of AudioStreams of which to concatenate together

        Returns:
            AudioStream representing the concatenated audio.
        """
        return self.audio_h.concat(streams)

    def overlay(
        self,
        left_stream : AudioStream,
        right_stream : AudioStream,
        loop_shorter_stream : bool = False
    ) -> AudioStream:
        """
        Overlays two audio streams on top of each other

        Args:
            left_stream:AudioStream
                stores one audio file data that will be overlayed 
            right_stream:AudioStream
                stores one audio file data that will be overlayed 
            loop_shorter_stream: bool
                if true, the shorter audio file will be looped until it reaches
                the length of the longer audio file 
        Returns:
            AudioStream representing the overlaid audio files.
        """
        return self.audio_h.overlay(
            left_stream, right_stream,loop_shorter_stream
        )

    def reverse(self, stream : AudioStream) -> AudioStream:
        """
        Reverse the given audio stream in place

        Args:
            stream: AudioStream to reverse

        Returns:
            AudioStream representing the reversed audio.
        """
        return self.audio_h.reverse(stream)

    def chunk(
        self,
        stream : AudioStream,
        chunk_duration_s : float
    ) -> List[AudioStream]:
        """
        Generates chunks of the given audio with the provided duration.

        Args:
            stream: AudioStream for which to generate chunks
            chunk_duration_s: float representing the duration to make each chunk

        Returns:
            A list of AudioStreams containing each generated chunk
        """
        return self.audio_h.chunk(
            stream, chunk_duration_s
        )

    ### Video Methods
    def extract_audio(self, stream : VideoStream) -> AudioStream:
        raise NotImplementedError

    def remove_audio(self, stream : VideoStream) -> VideoStream:
        raise NotImplementedError

    def _get_handler(self, stream : Stream) -> Union[AudioHandler, VideoHandler]:
        """
        Returns the handler of a given stream; either Audio or Video
        
        Args:
            stream for which to generate the handler
            
        Returns:
            AudioHandler or VideoHandler, depending on the type of the given stream. """
        return self.audio_h if isinstance(stream, AudioStream) else self.video_h
    
    @staticmethod
    def convert_to_16bit_wav(input_path, output_path):
        return AudioHandler.convert_to_16bit_wav(input_path, output_path)

        
    @staticmethod 
    def compress_to_opus(media_path:str, output_dir:str):
        """ compress the  file stored in media_path to output_dir, 
            with the same  file name with compressed format

        Args:
            media_path (str): the path to original file 
            output_dir (str): the path to the directory where the compressed file 
                              will be stored

        Raises:
            ChildProcessError: 
            ChildProcessError: 
            ProcessLookupError: 

        Returns:
            str: the path to the compressed file
        """
        return AudioHandler.compress_to_opus(media_path, output_dir)
    
    @staticmethod 
    def chunk_audio_to_outpath(input_path:str, output_path:str, duration:int) -> List[str]:
        """ given the audio path, chunking the audio into a series of audio
            segments
        
        Args:
            audiopath[str]: the file path to the audio file 
            output_path[str]: the output of the chunked file 
            duration[int]: the length of each chunk
            
        Return:
            Union[List[str], bool]: return a list of the audio path to the 
                                    chunked audios in order 
        """
        return AudioHandler.chunk_audio_to_outpath(input_path, output_path, duration)
    
    
    @staticmethod 
    def remove_prelude_silence(input_path:str, outdir:str) -> str:
        ouput_path = os.path.join(outdir, f"{get_name(input_path)}.{get_extension(input_path)}")
        sound = AudioSegment.from_file(input_path)
        leading_silence = detect_leading_silence(sound)
        trim_ed: AudioSegment = sound[leading_silence :]
        trim_ed.export(ouput_path, "wav")
        return ouput_path
