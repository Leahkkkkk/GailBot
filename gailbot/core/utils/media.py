# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 16:28:17
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-09 11:08:23

from typing import List, Union, Dict, Any
from dataclasses import dataclass
from pydub import AudioSegment
from .general import (
    get_extension,
    get_name
)
from .types import dtypes

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

    @property
    def supported_formats(self) -> List[str]:
        pass

    @staticmethod
    def is_supported(self, path : str) -> bool:
        pass

    def read_file(self, path : str) -> AudioStream:
        pass

    def record(
        self,
        name : str,
        out_dir : str,
        duration_sec : float = -1,
    ) -> AudioStream:
        pass

    def write_stream(
        self,
        stream : AudioStream,
        out_dir : str,
        name : str = None,
        extension : str = None
    ) -> str:
        pass

    def info(self, stream : AudioStream) -> Dict:
        pass

    def change_volume(
        self,
        stream : AudioStream,
        change_db : float
    ) -> AudioStream:
        pass

    def mono_to_stereo(
        self,
        left_stream : AudioStream,
        right_stream : AudioStream
    ) -> AudioStream:
        pass

    def stereo_to_mono(
        self,
        stream : AudioStream
    ) -> List[AudioStream]:
        pass

    def concat(self, streams : List[AudioStream]) -> AudioStream:
        pass

    def overlay(
        self,
        left_stream : AudioStream,
        right_stream : AudioStream
    ) -> AudioStream:
        pass

    def reverse(self, stream : AudioStream) -> AudioStream:
        pass

    def chunk(
        self,
        stream : AudioStream,
        chunk_duration_s : float
    ) -> List[AudioStream]:
        pass


class VideoHandler:

    @property
    def supported_formats(self) -> List[str]:
        pass

    @staticmethod
    def is_supported(self, path : str) -> bool:
        pass

    def read_file(self, path : str) -> VideoStream:
        pass

    def record(
        self,
        name : str,
        out_dir : str,
        duration_sec : float = -1,
    ) -> VideoStream:
        pass

    def write_stream(
        self,
        stream : VideoStream,
        out_dir : str,
        name : str = None,
        extension : str = None
    ) -> str:
        pass

    def info(self, stream : VideoStream) -> Dict:
        pass

    def change_volume(
        self,
        stream : VideoStream,
        change_db : float
    ) -> VideoStream:
        pass

    def extract_audio(self, stream : VideoStream) -> AudioStream:
        pass

    def remove_audio(self, stream : VideoStream) -> VideoStream:
        pass


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
        pass

    def change_volume(
        self,
        stream : Stream,
        change_db : float
    ) -> Stream:
        pass


    ### Audio Methods

    def mono_to_stereo(
        self,
        left_stream : AudioStream,
        right_stream : AudioStream
    ) -> AudioStream:
        pass

    def stereo_to_mono(
        self,
        stream : AudioStream
    ) -> List[AudioStream]:
        pass

    def concat(self, streams : List[AudioStream]) -> AudioStream:
        pass

    def overlay(
        self,
        left_stream : AudioStream,
        right_stream : AudioStream
    ) -> AudioStream:
        pass

    def reverse(self, stream : AudioStream) -> AudioStream:
        pass

    def chunk(
        self,
        stream : AudioStream,
        chunk_duration_s : float
    ) -> List[AudioStream]:
        pass

    ### Video Methods
    def extract_audio(self, stream : VideoStream) -> AudioStream:
        pass

    def remove_audio(self, stream : VideoStream) -> VideoStream:
        pass

    def _get_handler(self, stream : Stream) -> Union[AudioHandler, VideoHandler]:
        return self.audio_h if isinstance(stream, AudioStream) else self.video_h







