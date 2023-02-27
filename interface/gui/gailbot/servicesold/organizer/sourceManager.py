# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 14:50:11
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-16 15:32:33
from typing import List, Dict, Any, Callable
from gailbot.core.utils.general import (
    is_directory,
    read_toml,
    is_file,
    write_toml,
    make_dir,
    filepaths_in_dir,
    get_extension,
    get_name,
    delete
)
from gailbot.core.utils.media import MediaHandler
from gailbot.servicesold.pipeline.objects import PayloadOutputWriter  
# NOTE: want to get rid of the above line of import 
from .objects import Source, DataFile



# TODO: These loaders should be somewhere else.
# Loaders for sources
class SourceLoader:

    def __call__(self, *args, **kwargs):
        raise NotImplementedError()


class AudioSourceLoader(SourceLoader):

    def __init__(self):
        self.media_h = MediaHandler()

    def __call__(
        self,
        source_name : str,
        source_path : str,
        output_dir : str,
    ) -> Source:

        if not self.media_h.is_audio(source_path):
            return

        data_file = DataFile(source_path)
        return Source(
            identifier=source_name,
            workspace_dir=output_dir,
            data_files=[data_file],
            settings_profile=None
        )

class VideoSourceLoader(SourceLoader):

    def __init__(self):
        self.media_h = MediaHandler()

    def __call__(
        self,
        source_name : str,
        source_path : str,
        output_dir : str
    ) -> Source:

        if not self.media_h.is_video(source_path):
            return

        # NOTE: Any audio / video extraction happens in the pipeline, not here.
        data_file = DataFile(source_path)
        return Source(
            identifier=source_name,
            workspace_dir=output_dir,
            data_files=[data_file],
            settings_profile=None
        )


class ConversationDirectorySourceLoader(SourceLoader):
    """ NOTE: loading the entire directory instead of just single file  """
    def __init__(self):
        self.media_h = MediaHandler()

    def __call__(
        self,
        source_name : str,
        source_path : str,
        output_dir : str
    ) -> Source:

        if not is_directory(source_path):
            return

        paths = filepaths_in_dir(
            source_path,self.media_h.supported_formats(),recursive=False
        )
        data_files = [DataFile(path) for path in paths]
        return Source(
            identifier=source_name,
            workspace_dir=output_dir,
            data_files=data_files,
            settings_profile=None
        )

# TODO: Implement later based on the final directory output structure.
class TranscribedOutputSourceLoader(SourceLoader):
    """ loading the transcribed output - only used when we need to 
        re-transcribe something 
    """

    def __call__(
        self,
        source_name : str,
        source_path : str,
        output_dir : str
    ) -> Source:


        if not is_directory(source_path) or \
                not PayloadOutputWriter.is_payload_output(source_path):
            return

        return PayloadOutputWriter.read_payload_output(source_path)


class SourceManager:
    """Simply creates and manages the workspace for sources"""
    def __init__(self, workspace_dir : str):
        self.workspace_dir = workspace_dir
        make_dir(workspace_dir,overwrite=True)
        self.loaders = [
            AudioSourceLoader(),
            VideoSourceLoader(),
            ConversationDirectorySourceLoader(),
            TranscribedOutputSourceLoader()
        ]
        self.sources : Dict[str, Source] = dict()

    def add_source(
        self,
        source_name : str,
        source_path : str,
    ) -> bool:

        for loader in self.loaders:
            out_dir = f"{self.workspace_dir}/{source_name}"
            source = loader(source_name, source_path, out_dir)
            if isinstance(source, Source):
                break
        if source == None or self.is_source(source_name):
            return False

        self.sources[source_name] = source
        return True

    def remove_source(self, source_name : str) -> bool:
        if self.is_source(source_name):
            del self.sources[source_name]
            return True
        return False

    def is_source(self, source_name : str) -> bool:
        return source_name in self.sources

    def source_names(self) -> List[str]:
        return list(self.sources.keys())

    def get_source(self, source_name : str) -> Source:
        if self.is_source(source_name):
            return self.sources[source_name]

    def map_sources(self, fn : Callable) -> Dict:
        res = dict()
        for name, source in self.sources.items():
            res[name] = fn(source)
        return res

    def get_source_details(self, source_name : str) -> Dict:
        if self.is_source(source_name):
            return self.sources[source_name].to_dict()
