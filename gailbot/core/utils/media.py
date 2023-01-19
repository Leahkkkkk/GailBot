# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 16:28:17
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-14 15:18:45

from typing import List, Union, Dict, Any
from dataclasses import dataclass
from pydub import AudioSegment
from .general import (
    get_extension,
    get_name,
    make_dir
)

@dataclass
class Stream:
    source : Union[List[str], List["Stream"]]
    name : str
    extension : str

@dataclass
class AudioStream(Stream):
    segment : AudioSegment

    def __repr__(self):
        pass

@dataclass
class VideoStream(Stream):
    pass

    def __repr__(self):
        pass

class AudioHandler:

    _SUPPORTED_FORMATS = ["mp3", "mpeg", "opus", "wav"]
    _DEFAULT_FORMAT = "wav"

    @property
    def supported_formats(self) -> List[str]:
        return self._SUPPORTED_FORMATS

    @staticmethod
    def is_supported(self, path : str) -> bool:
        return get_extension(path) in self.supported_formats

    def read_file(self, path : str) -> AudioStream:
        """
        Read a file as a stream
        """
        if not self.is_supported(self, path):
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
        raise NotImplementedError()

    def write_stream(
        self,
        stream : AudioStream,
        outdir : str,
        name : str = None,
        format : str = None
    ) -> str:
        """
        Write a stream with the given format. If not format or name is specified,
        uses the stream's default name and format.
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
        """Get information about the given audio stream"""
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
                "num_frames": segment.frame_count()
        }

    def change_volume(
        self,
        stream : AudioStream,
        change_db : float
    ) -> AudioStream:
        """
        Apply the specified gain to the audio stream.
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
        Get a new stereo stream from the mono streams
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
        """

        left_segment,right_segment = stream.segment.split_to_mono()
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
        """
        concatenated = AudioSegment.empty()
        for stream in streams:
            concatenated += stream.segment
        name = "_".join([stream.name for stream in streams])
        name += "_concatenated"
        return AudioStream(
            sources=[streams],
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
        Reverse the given audio stream in place
        """
        reversed_segment = stream.segment.reverse
        stream.segment = reversed_segment
        return stream

    def chunk(
        self,
        stream : AudioStream,
        chunk_duration_s : float
    ) -> List[AudioStream]:
        """
        Generate chunks of the given audio with the provided duration.
        """
        assert chunk_duration_s > 0, f"Duration must be positive"

        # Simply return original stream if no chunking possible.
        if chunk_duration_s < stream.segment.duration_seconds:
            return [stream]

        duration_ms = chunk_duration_s * 1000
        chunks = list()
        for i, chunk_segment in enumerate(stream.segment[::duration_ms]):
            name = f"{stream.name}_{chunk_duration_s}_chunk_{i}"
            chunk = AudioStream(
                [stream],name, self._DEFAULT_FORMAT,chunk_segment
            )
            chunks.append(chunk)
        return chunks

# TODO: Implement methods.
class VideoHandler:

    _SUPPORTED_FORMATS = "mxf"
    _BASE_FORMAT = "mp4"

    @property
    def supported_formats(self) -> List[str]:
        return self._SUPPORTED_FORMATS

    @staticmethod
    def is_supported(self, path : str) -> bool:
        return get_extension(path) in self.supported_formats

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
        self.audio_h = AudioHandler()
        self.video_h = VideoHandler()

    @property
    def supported_formats(self) -> List[str]:
        return self.audio_h.supported_formats + self.video_h.supported_formats

    #### Audio and Video

    @staticmethod
    def is_audio(self, path : str) -> bool:
        return AudioHandler.is_supported(path)

    @staticmethod
    def is_video(self, path : str) -> bool:
        return VideoHandler.is_supported(path)

    def read_file(self, path : str) -> Stream:
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
        if out_stream_type == AudioStream:
            return self.audio_h.record(name, out_dir, duration_sec)
        else:
            return self.video_h.record(name, out_dir, duration_sec)


    def write_stream(
        self,
        stream : Stream,
        out_dir : str,
        name : str = None,
        extension : str = None
    ) -> str:
        return self._get_handler(stream).write_stream(
            stream, out_dir, name, extension
        )

    def info(self, stream : Stream) -> Dict:
        return self._get_handler(stream).info(stream)

    def change_volume(
        self,
        stream : Stream,
        change_db : float
    ) -> Stream:
        return self._get_handler(stream).change_volume(stream)

    ### Audio Methods

    def mono_to_stereo(
        self,
        left_stream : AudioStream,
        right_stream : AudioStream
    ) -> AudioStream:
        return self.audio_h.mono_to_stereo(left_stream, right_stream)

    def stereo_to_mono(
        self,
        stream : AudioStream
    ) -> List[AudioStream]:
        return self.audio_h.stereo_to_mono(stream)

    def concat(self, streams : List[AudioStream]) -> AudioStream:
        return self.audio_h.concat(streams)

    def overlay(
        self,
        left_stream : AudioStream,
        right_stream : AudioStream,
        loop_shorter_stream : bool = False
    ) -> AudioStream:
        return self.audio_h.overlay(
            left_stream, right_stream,loop_shorter_stream
        )

    def reverse(self, stream : AudioStream) -> AudioStream:
        return self.audio_h.reverse(stream)

    def chunk(
        self,
        stream : AudioStream,
        chunk_duration_s : float
    ) -> List[AudioStream]:
        return self.audio_h.chunk(
            stream, chunk_duration_s
        )

    ### Video Methods
    def extract_audio(self, stream : VideoStream) -> AudioStream:
        pass

    def remove_audio(self, stream : VideoStream) -> VideoStream:
        pass

    def _get_handler(self, stream : Stream) -> Union[AudioHandler, VideoHandler]:
        return self.audio_h if isinstance(stream, AudioStream) else self.video_h







