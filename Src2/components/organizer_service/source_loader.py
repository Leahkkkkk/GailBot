# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-02 14:12:19
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2021-12-02 16:28:11

from ..io import IO
from ..shared_models import Source, SourceHook, Conversation, DataFile


class SourceLoader:

    def __init__(self,) -> None:

        self.io = IO()
        self.loaders = [FileLoader()]

    ################################# MODIFIERS #########################

    def load_source(self, source_name: str, source_path: str,
                    result_dir_path: str, transcriber_name: str) -> Source:

        for loader in self.loaders:
            source = loader.load(source_name, source_path,
                                 result_dir_path, transcriber_name)
            if source != None:
                return source


class FileLoader:

    def __init__(self):
        self.io = IO()

    def load(self, source_name: str, source_path: str,
             result_dir_path: str, transcriber_name: str) -> Source:
        source_extension = self.io.get_file_extension(source_path)
        if not self.io.is_file(source_path):
            return
        data_file = DataFile(source_path, source_path, None)
        conversation = Conversation([data_file])
        hook = SourceHook(
            result_dir_path, source_name, result_dir_path)
        return Source(source_name, conversation, hook)
