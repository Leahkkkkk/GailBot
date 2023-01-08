# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 14:50:11
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-08 16:13:40

from typing import List, Dict, Any

from ..baseObjects.objects import Source


# Loaders for sources
class SourceLoader:

    def load(self, *args, **kwargs):
        raise NotImplementedError()


class AudioSourceLoader(SourceLoader):

    def __init__(self):
        pass

    def load(self):
        pass

class VideoSourceLoader(SourceLoader):

    def __init__(self):
        pass

    def load(self):
        pass

class ConversationDirectorySourceLoader(SourceLoader):

    def __init__(self):
        pass

    def load(self):
        pass

class TranscribedOutputSourceLoader(SourceLoader):

    def __init__(self):
        pass

    def load(self):
        pass


class SourceManager:

    def __init__(self):
        pass

    def add_source(
        self,
        source_name : str,
        source_path : str,
        output_dir : str
    ) -> bool:
        pass

    def remove_source(self, source_name : str) -> bool:
        pass

    def is_source(self, source_name : str) -> bool:
        pass

    def configured_sources(self) -> List[Source]:
        pass

    def configured_source_names(self) -> List[str]:
        pass

    def get_source_details(self, source_name : str) -> Dict:
        pass