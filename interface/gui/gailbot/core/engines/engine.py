# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-06 15:49:53
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-09 11:21:54

from abc import ABC, abstractmethod
from typing import List
from typing import Any, Dict

class Engine(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def __repr__(self):
        """Returns all the configurations and additional metadata"""
        raise NotImplementedError()
    
    @abstractmethod
    def transcribe(self, *args, **kwargs) -> Any:
        """Use the engine to transcribe an item"""
        pass
    
    @abstractmethod
    def was_transcription_successful(self) -> bool:
        """ return true if the transcription is successful """
        pass 

    @abstractmethod
    def get_engine_name(self) -> str:
        """
        Obtain the name of the current engine.

        Returns:
            (str): Name of the engine.
        """
        pass

    @abstractmethod
    def get_supported_formats(self) -> List[str]:
        """
        Obtain a list of audio file formats that are supported.

        Returns:
            (List[str]): Supported audio file formats.
        """
        pass

    @abstractmethod
    def is_file_supported(self, file_path: str) -> bool:
        """
        Determine if the given file is supported by the engine.

        Args:
            file_path (str)

        Returns:
            (bool): True if file is supported. False otherwise.
        """
        pass
    
    
    







