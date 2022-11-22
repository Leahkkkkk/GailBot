# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-02 14:12:19
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-08-23 11:41:56
from typing import List
from gailbot.core.io import GailBotIO
from gailbot.services.objects import (
    Source,
    SourceHook,
    Settings,
    SettingsHook,
    SettingsProfile,
    GailBotSettings,
    DataFile,
    Conversation
)
class SourceLoader:

    def __init__(self,) -> None:

        self.io = GailBotIO()
        self.loaders = [AudioFileLoader(), VideoFileLoader(),
                        TranscribedDirectoryLoader(),
                        DirectoryLoader()]

    ################################# MODIFIERS #########################

    def load_source(self, source_name: str, source_path: str,
                    result_dir_path: str, temp_ws_path: str) -> Source:
        # Search through all the source loaders and use the appropriate one.
        for loader in self.loaders:
            source = loader.load(
                source_name, source_path, result_dir_path, temp_ws_path)
            if source != None:
                return source


class AudioFileLoader:

    def __init__(self):
        self.io = GailBotIO()

    def load(self, source_name: str, source_path: str,
             result_dir_path: str, temp_ws_path: str)\
            -> Source:
        if not self.io.is_file(source_path) or \
                not self.io.is_supported_audio_file(source_path):
            return

        data_file = DataFile(
            self.io.get_name(source_path),
            source_path, source_path, None)
        conversation = Conversation([data_file])
        hook = SourceHook(
            source_name, temp_ws_path, result_dir_path)
        return Source(source_name, conversation, hook)

    def get_data_files(self) -> List[DataFile]:
        pass


class VideoFileLoader:

    def __init__(self):
        self.io = GailBotIO()

    def load(self, source_name: str, source_path: str,
             result_dir_path: str,  temp_ws_path: str)\
            -> Source:
        if not self.io.is_file(source_path) or \
                not self.io.is_supported_video_file(source_path):
            return
        # Create the hook first
        hook = SourceHook(
            source_name, temp_ws_path, result_dir_path)
        # Extract audio from the video
        # NOTE: Assuming only one audio extracted
        audio_path = self.io.extract_audio_from_file(
            source_path, hook.get_temp_directory_path())
        if audio_path == None:
            return False
        data_files = list()
        for path in [audio_path]:
            data_file = DataFile(
                self.io.get_name(path), source_path, path, source_path)
            data_files.append(data_file)
        conversation = Conversation(data_files)

        return Source(source_name, conversation, hook)


class DirectoryLoader:

    def __init__(self):
        self.io = GailBotIO()

    def load(self, source_name: str, source_path: str,
             result_dir_path: str,  temp_ws_path: str)\
            -> Source:
        if not self.io.is_directory(source_path):
            return
        paths = self.io.path_of_files_in_directory(
            source_path, ["*"], False)
        data_files = list()
        # Create the hook
        hook = SourceHook(
            source_name, temp_ws_path, result_dir_path)
        # Load the files
        for path in paths:
            if self.io.is_supported_audio_file(path):
                data_files.append(
                    DataFile(self.io.get_name(path), path, path, None))
            elif self.io.is_supported_video_file(path):
                audio_path = self.io.extract_audio_from_file(
                    path,  hook.get_temp_directory_path())
                if audio_path != None:
                    for audio in [audio_path]:
                        data_file = DataFile(
                            self.io.get_name(audio), path, audio, path)
                        data_files.append(data_file)
        conversation = Conversation(data_files)
        return Source(source_name, conversation, hook)


class TranscribedDirectoryLoader:

    def __init__(self):
        self.io = GailBotIO()

    def load(self, source_name: str, source_path: str,
             result_dir_path: str,  temp_ws_path: str) \
            -> Source:
        if not self.io.is_directory(source_path):
            return
        # Check whether metadata file exists.
        paths = self.io.path_of_files_in_directory(
            source_path, ["json"], False)
        if len(paths) != 1:
            return
        # Otherwise, attempt to parse
        metadata = self.io.read(paths[0])[1]
        loaded_data_files = metadata["data_files"]
        data_files = list()
        for identifier, data in loaded_data_files.items():
            raw_path = "{}/{}".format(
                source_path, data["generated_paths"]["raw"])
            audio_path = "{}/{}".format(
                source_path, data["generated_paths"]["media"])
            if not self.io.is_file(raw_path) or not self.io.is_file(audio_path):
                continue
            data_file = DataFile(identifier, raw_path, audio_path, None)
            data_files.append(data_file)
        # Create the Source
        conversation = Conversation(data_files)
        hook = SourceHook(
            source_name, temp_ws_path, result_dir_path)
        return Source(source_name, conversation, hook)
