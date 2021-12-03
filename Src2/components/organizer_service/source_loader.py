# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-02 14:12:19
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2021-12-02 18:43:35

from ..io import IO
from ..shared_models import Source, SourceHook, Conversation, DataFile


class SourceLoader:

    def __init__(self,) -> None:

        self.io = IO()
        self.loaders = [AudioFileLoader()]

    ################################# MODIFIERS #########################

    def load_source(self, source_name: str, source_path: str,
                    result_dir_path: str, transcriber_name: str,
                    temp_ws_path: str) -> Source:

        for loader in self.loaders:
            source = loader.load(source_name, source_path,
                                 result_dir_path, transcriber_name, temp_ws_path)
            if source != None:
                return source


class AudioFileLoader:

    def __init__(self):
        self.io = IO()

    def load(self, source_name: str, source_path: str,
             result_dir_path: str, transcriber_name: str, temp_ws_path: str)\
            -> Source:
        if not self.io.is_file(source_path):
            return
        data_file = DataFile(source_path, source_path, None)
        conversation = Conversation([data_file])
        hook = SourceHook(
            temp_ws_path, source_name, result_dir_path)
        return Source(source_name, conversation, hook)


class VideoFileLoader:

    def __init__(self):
        self.io = IO()

    def load(self, source_name: str, source_path: str,
             result_dir_path: str, transcriber_name: str, temp_ws_path: str)\
            -> Source:
        if not self.io.is_directory(source_path) or \
                not self.io.is_supported_video_file(source_path):
            return False
        # Extract audio from the video
        # NOTE: Assuming only one audio extracted
        audio_path = self.io.extract_audio_from_file(source_path, temp_ws_path)
        data_files = list()
        for path in [audio_path]:
            data_file = DataFile(source_path, path, source_path)
            data_files.append(data_file)
        conversation = Conversation(data_files)
        hook = SourceHook(
            temp_ws_path, source_name, result_dir_path)
        return Source(source_name, conversation, hook)
